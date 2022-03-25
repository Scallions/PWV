import paddle
import paddle.optimizer
import paddle.nn
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model.dcgenerator import DCGenerator
from data.pwv import PWVDataset
from visualdl import LogWriter


gps_data = "../pwv_1h_hz_grl_filter_miss.csv"
era_data = "../pwv.nc"

G = DCGenerator(35, 1)
ds = PWVDataset(gps_data, era_data)
dsl = int(0.8*len(ds))
tsl = len(ds) - dsl
ds, ts = paddle.io.random_split(ds, [dsl,tsl])
ds = paddle.io.DataLoader(ds, batch_size=64, shuffle=True)
ts = paddle.io.DataLoader(ts, batch_size=512, shuffle=True)
# opt = paddle.optimizer.Adam(0.0002, parameters=G.parameters())
lr = paddle.optimizer.lr.PolynomialDecay(0.0002, len(ds), 1e-6)
# opt = paddle.optimizer.SGD(lr, parameters=G.parameters())
opt = paddle.optimizer.Adam(lr, parameters=G.parameters())
loss = paddle.nn.MSELoss()
epoch = 100

step = 0
best_l = 1e5
with LogWriter(logdir="./log/vd") as writer:
    obar = tqdm(range(epoch))
    for epoch in obar:
        bar = tqdm(ds, leave=False)
        G.train()
        for bs, (gps, era) in enumerate(bar):
            step += 1
            pp = G(gps)
            l = loss(pp, era)
            l.backward()
            opt.step()
            opt.clear_grad()
            if bs % (max(len(ds)//10,1)) == 0:
                bar.set_description(f"L: {l.numpy().item():.5e}")
                # print(pp.mean().item(), pp.sum().item())
                writer.add_scalar(tag="train", step=step, value=l.numpy().item())

        ## 测试集测试
        G.eval()
        for gps, era in ts:
            pp = G(gps)
            l = loss(pp, era)
        if l.numpy().item() < best_l:
            paddle.save(G.state_dict(), "out/G_best.pdmodel")
            best_l = l.numpy().item()
        obar.set_description(f"L: {l.numpy().item():.5e}")
        writer.add_scalar(tag="test", step=step, value=l.numpy().item())
        writer.add_image(tag="predict",
                             img=pp[0,:,:].detach().numpy(),
                             step=step,
                             dataformats="HW",
                             )
        writer.add_image(tag="true",
                             img=era[0,:,:].detach().numpy(),
                             step=step,
                             dataformats="HW",
                             )
        # max_ = pp[0].max().item()+0.1
        # min_ = pp[0].min().item()-0.1
        max_ = 1
        min_ = 0
        plt.figure()
        plt.title(f"P L: {l.numpy().item():.5e}")
        plt.imshow(pp[0,:,:].detach().numpy(),cmap='terrain',vmin=min_, vmax=max_)
        plt.colorbar()
        plt.savefig(f"out/{epoch}_p.png")
        plt.close()
        plt.figure()
        plt.title(f"T L: {l.numpy().item():.5e}")
        plt.imshow(era[0,:,:].detach().numpy(),cmap='terrain',vmin=min_, vmax=max_)
        plt.colorbar()
        plt.savefig(f"out/{epoch}_t.png")
        plt.close()

    print(f"Last L: {l.numpy().item():.5e}")
    paddle.save(G.state_dict(), "out/G_last.pdmodel")
