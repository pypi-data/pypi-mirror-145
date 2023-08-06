from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
import os
# from criterion import *
# from my_operator import *
import seaborn as sns
import k3d

def vis_tensor(beta):
    volume = k3d.volume(beta)
    plot = k3d.plot(camera_auto_fit=True)
    plot += volume
    plot.lighting = 2
    plot.display()

# def ni_show(beta_hat,threshold = 0,cut_coords = None,save_name = None):
#     ss = 3
#     file_name = "1497923_20252_2_0"  ##1496176_20252_2_0
#     data_dir = r"C:\Users\student\Desktop\Ukbiobank\20252"
#     img = nib.load(os.path.join(data_dir,file_name,"T1/T1_brain_to_MNI.nii.gz"))
#     re_th = resize(beta_hat,(144,184,144))
#     canvas = np.zeros(list(img.dataobj.shape))
#     canvas[7+4*ss:-7-4*ss,5+4*ss:-5-4*ss,4*ss-4:-18-4*ss] = re_th
#     new_image = nib.Nifti1Image(fun_normalization(canvas), img.affine)
#     fig = plt.figure(figsize=(9, 3), facecolor='w')
#     # background = new_img_like(img,new_image)
#     out_dir = r"C:\Users\student\OneDrive - City University of Hong Kong\pycharm\SKPD_server"
#     if not save_name is None:
#         save_name = os.path.join(out_dir,save_name)

#     display = plot_stat_map(stat_map_img = new_image,bg_img = img,
#                             threshold=threshold,
#                             colorbar = True,
#                             draw_cross = False,
#                             cut_coords= cut_coords,
#                             black_bg = False,
#                             output_file = save_name,
#                             figure=fig)
#     show()