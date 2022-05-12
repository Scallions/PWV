import paddle
import paddle.optimizer
import paddle.nn
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model.dcgenerator import DCGenerator
from model.dcdiscriminator import DCDiscriminator
from data.pwv import PWVDataset
from visualdl import LogWriter
import numpy as np

class GradientPenalty():
    def __init__(self, loss_weight=1.0):
        self.loss_weight = loss_weight

    def __call__(self, net, real, fake):
        batch_size = real.shape[0]
        alpha = paddle.rand([batch_size])
        for _ in range(real.ndim - 1):
            alpha = paddle.unsqueeze(alpha, -1)
        interpolate = alpha * real + (1 - alpha) * fake
        interpolate.stop_gradient = False
        interpolate_pred, _ = net(interpolate)
        gradient = paddle.grad(outputs=interpolate_pred,
                               inputs=interpolate,
                               grad_outputs=paddle.ones_like(interpolate_pred),
                               create_graph=True,
                               retain_graph=True,
                               only_inputs=True)[0]
        gradient_penalty = ((gradient.norm(2, 1) - 1) ** 2).mean()
        return gradient_penalty * self.loss_weight

gps_data = "../pwv_1h_hz_grl_long_fill.csv"
era_data = "/home/aistudio/data/data144997/pwv.nc"

G = DCGenerator(2000, 24)
D = DCDiscriminator(24)
dsa = PWVDataset(gps_data, era_data)
dsl = int(0.9*len(dsa))
tsl = len(dsa) - dsl
# ds, ts = paddle.io.random_split(ds, [dsl,tsl])
from paddle.io import Subset
# all_idx = list(range(len(dsa)))
# import random
# random.shuffle(all_idx)
# train_idxs = all_idx[:dsl]
# test_idxs = all_idx[dsl:]
train_idxs = range(0, dsl)
test_idxs = range(dsl, len(dsa))
# import pickle
# with open("idxs_train.pkl", "wb") as f:
#     pickle.dump(train_idxs, f, 0)
# with open("idxs_test.pkl", "wb") as f:
#     pickle.dump(test_idxs, f, 0)
ts = Subset(dataset=dsa, indices=train_idxs)
ds = Subset(dataset=dsa, indices=test_idxs)
dl = paddle.io.DataLoader(ds, batch_size=64, shuffle=False)
tl = paddle.io.DataLoader(ts, batch_size=512, shuffle=True)
# opt = paddle.optimizer.Adam(0.0002, parameters=G.parameters())
# lr = paddle.optimizer.lr.PolynomialDecay(0.0002, len(ts), 1e-5, cycle=True)
lr = 0.0002
# opt = paddle.optimizer.SGD(lr, parameters=G.parameters())
# opt = paddle.optimizer.Adam(lr, parameters=G.parameters())
# optD = paddle.optimizer.Adam(lr, parameters=D.parameters())
# optI = paddle.optimizer.Adam(lr, parameters=G.parameters()+D.parameters())
clip = paddle.nn.ClipGradByValue(min=-0.01, max=0.01)
# opt = paddle.optimizer.SGD(lr, parameters=G.parameters(), grad_clip=clip)
opt = paddle.optimizer.Adam(lr, parameters=G.parameters())
optD = paddle.optimizer.Adam(lr, parameters=D.parameters())
optI = paddle.optimizer.Adam(lr, parameters=G.parameters()+D.parameters())
loss = paddle.nn.MSELoss()
gp = GradientPenalty()
# loss = paddle.nn.BCELoss()
epoch = 400

step = 0
best_l = 1e5

def log(writer, obar):
    global best_l
    ## 测试集测试
    G.eval()
    ls = []
    for gps, era in dl:
        pp = G(gps)
        pg, _ = D(pp)
        # l = loss(pg, paddle.ones_like(pg))
        # l1 = loss(pg, paddle.ones_like(pg))
        l1 = paddle.mean(pg)
        l2 = lloss(pp, era)
        lg = l1 + 2*l2 # + l1*l2
        # l = loss(pp, era)
        ls.append(lg.numpy().item())
    l = np.mean(ls).item()
    if l < best_l:
        paddle.save(G.state_dict(), "out/G_best.pdmodel")
        best_l = l
    obar.set_description(f"L: {l:.5e}")
    writer.add_scalar(tag="test/lg", step=step, value=l)
    writer.add_image(tag="predict",
                            img=pp[0,0,:,:].detach().numpy(),
                            step=step,
                            dataformats="HW",
                            )
    writer.add_image(tag="true",
                            img=era[0,0,:,:].detach().numpy(),
                            step=step,
                            dataformats="HW",
                            )
    # max_ = pp[0].max().item()+0.1
    # min_ = pp[0].min().item()-0.1
    max_ = 1
    min_ = 0
    plt.figure()
    plt.title(f"P L: {l:.5e}")
    plt.imshow(pp[0,0,:,:].detach().numpy(),cmap='terrain',vmin=min_, vmax=max_)
    plt.colorbar()
    plt.savefig(f"out/{epoch}_p.png")
    plt.close()
    plt.figure()
    plt.title(f"T L: {l:.5e}")
    plt.imshow(era[0,0,:,:].detach().numpy(),cmap='terrain',vmin=min_, vmax=max_)
    plt.colorbar()
    plt.savefig(f"out/{epoch}_t.png")
    plt.close()
# print(len(tl))

lloss = paddle.nn.MSELoss()
obar = tqdm(range(3))
for e in obar:
    bar = tqdm(tl, leave=False)
    G.train()
    for bs, (gps, era) in enumerate(bar):
        opt.clear_grad()
        step += 1
        pp = G(gps)
        l = lloss(pp, era)
        l.backward()
        opt.step()
        # lr.step()
        if (bs % (max(len(tl)//10,1))) == 0:
            bar.set_description(f"L: {l.numpy().item():.5e}")
    max_ = 1
    min_ = 0
    plt.figure()
    plt.title(f"P L: {l.item():.5e}")
    plt.imshow(pp[0,0,:,:].detach().numpy(),cmap='terrain',vmin=min_, vmax=max_)
    plt.colorbar()
    plt.savefig(f"out/p{e}_p.png")
    plt.close()
    plt.figure()
    plt.title(f"T L: {l.item():.5e}")
    plt.imshow(era[0,0,:,:].detach().numpy(),cmap='terrain',vmin=min_, vmax=max_)
    plt.colorbar()
    plt.savefig(f"out/p{e}_t.png")
    plt.close()


with LogWriter(logdir="./log/vd") as writer:
    obar = tqdm(range(epoch))
    ## 起步测试
    log(writer, obar)

    for epoch in obar:
        bar = tqdm(tl, leave=False)
        G.train()
        D.train()
        for bs, (gps, era) in enumerate(bar):
            step += 1
            ## D
            # for i in range(3):
            optD.clear_grad()
            p, _ = D(era)
            pp = G(gps)
            pg, _ = D(pp)
            # ld = loss(p, paddle.ones_like(p)) + loss(pg, paddle.zeros_like(pg))
            # ld = loss(p, paddle.ones_like(p)) + loss(pg, -1*paddle.ones_like(pg))
            # ld = ld / 2
            ld = paddle.mean(p) + -paddle.mean(pg) + gp(D, era, pp)
            ld.backward()
            optD.step()
            ## G
            opt.clear_grad()
            pp = G(gps)
            pg, _ = D(pp)
            # l1 = loss(pg, paddle.ones_like(pg))
            l1 = paddle.mean(pg)
            l2 = lloss(pp, era)
            lg = l1 + 2*l2 # + l1*l2
            # lg = lg / 2
            lg.backward()
            opt.step()
            ## I
            optI.clear_grad()
            b = gps.shape[0]
            code_r = paddle.randn([b,24,64])
            pp = G(code_r)
            _, code_p = D(pp)
            li = lloss(code_r, code_p)
            li.backward()
            optI.step()

            # lr.step()
            if (bs % (max(len(tl)//10,1))) == 0:
                bar.set_description(f"Lg:{lg.numpy().item():.4e},Ld:{ld.numpy().item():.4e},Li:{li.numpy().item():.4e}")
                # print(pp.mean().item(), pp.sum().item())
                writer.add_scalar(tag="train/ld", step=step, value=ld.numpy().item())
                writer.add_scalar(tag="train/lg", step=step, value=lg.numpy().item())
                writer.add_scalar(tag="train/li", step=step, value=li.numpy().item())

        ## 测试集测试
        log(writer, obar)
        paddle.save(G.state_dict(), "out/G_latest.pdmodel")

    print(f"Last L: {lg.numpy().item():.5e}")
    paddle.save(G.state_dict(), "out/G_last.pdmodel")
