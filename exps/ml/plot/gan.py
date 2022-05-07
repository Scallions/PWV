import gif
import numpy as np

data_dir = "/Volumes/HDD/Data/ztd/"

eras = np.load()

rmse = []
@gif.frame
def plot(pidx):
    # plt.title(f"{pidx}")
    cdata = startp + timedelta(hours=pidx+16*24)
    fig, axs = plt.subplots(1,2, subplot_kw={'projection': PlateCarree()})
    ax = axs[0]
    ax.set_title(f"GPS:{cdata}")
    ax.set_extent([-75,-12,55,85])
    ax.coastlines()
    # ax.gridlines(draw_labels=True)
    x = np.arange(-75, -11)
    y = np.arange(55, 86)
    xs, ys = np.meshgrid(x,y)
    mesh = ax.pcolormesh(xs, ys, out[pidx,:,:], vmin=vmin, vmax= vmax, transform=PlateCarree(), cmap = cmap)
    # plt.imshow(out[pidx,:,:])
    # plt.axis('off')
    ax = axs[1]
    ax.set_title(f"ERA:{cdata}")
    ax.set_extent([-75,-12,55,85])
    ax.coastlines()
    # ax.gridlines(draw_labels=True)
    x = np.arange(-75, -11)
    y = np.arange(55, 86)
    xs, ys = np.meshgrid(x,y)
    era = eras.sel(time=cdata).values[:31,:64][::-1,:]
    erass.append(era)
    mesh = ax.pcolormesh(xs, ys, era, vmin=vmin, vmax=vmax, transform=PlateCarree(), cmap=cmap)
    # plt.colorbar(ax=ax)
    fig.colorbar(mesh, ax=axs, orientation='horizontal')
    # plt.tight_layout()
    rmse.append(np.sqrt(np.mean((out[pidx,:,:]-era)**2)))

frames = []
erass = []
for i in range(timel):
    frame = plot(i)
    frames.append(frame)

# np.save("eras.npy", np.array(erass))
# np.save("outs.npy", out[:timel,:,:])

gif.save(frames, f"fig/gan.gif", duration=5, unit="s", between="startend")
print(np.mean(rmse))