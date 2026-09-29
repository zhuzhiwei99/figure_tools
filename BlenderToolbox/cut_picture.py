import os
import cv2
from test_mesh_path import *
from PIL import Image, ImageDraw, ImageMath


import cv2
import numpy as np

def sphere_cut_antialiased_cv2(fig_dir, imgname, cx, cy, radius, lwidth, cr='red'): # cx, cy are center
    if cr == 'red':
        color_bgr = (0, 0, 255, 255) # OpenCV uses BGR by default for color, alpha last
    elif cr == 'green':
        color_bgr = (0, 255, 0, 255)
    elif cr == 'blue':
        color_bgr = (255, 0, 0, 255)
    elif cr == 'gray':
        color_bgr = (90, 90, 90, 255)
    else:
        print('Warning: Invalid color, use red instead.')
        color_bgr = (0, 0, 255, 255)

    img_path = os.path.join(fig_dir, imgname)
    bbx_fig_dir = os.path.join(fig_dir, f'cx{cx}_cy{cy}_r{radius}_l{lwidth}/bbx_aa_cv2')
    os.makedirs(bbx_fig_dir, exist_ok=True)

    # Read image with Alpha channel using OpenCV
    image_cv = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    if image_cv is None:
        print(f"Error: Could not load image with OpenCV: {img_path}")
        return
    
    # Ensure it's BGRA if it has 4 channels
    if image_cv.shape[2] == 3: # If only BGR, add alpha
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2BGRA)
    
    # cv2.circle takes center coordinates and radius
    # thickness < 0 means filled circle. For outline, use positive thickness.
    # lineType=cv2.LINE_AA enables anti-aliasing
    cv2.circle(image_cv, (cx, cy), radius, color_bgr, thickness=lwidth, lineType=cv2.LINE_AA)
    
    output_path = os.path.join(bbx_fig_dir, imgname[:-4] + '_sbbx_aa_cv2_' + cr + '.png')
    cv2.imwrite(output_path, image_cv)
    print(f"Saved anti-aliased image with CV2: {output_path}")

    # For anti-aliased circular cut with OpenCV:
    cut_fig_dir = os.path.join(fig_dir, f'cx{cx}_cy{cy}_r{radius}_l{lwidth}/cut_aa_cv2')
    os.makedirs(cut_fig_dir, exist_ok=True)

    original_for_cut = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    if original_for_cut is None: return
    if original_for_cut.shape[2] == 3:
        original_for_cut = cv2.cvtColor(original_for_cut, cv2.COLOR_BGR2BGRA)
    
    # Create mask
    mask_cv = np.zeros((original_for_cut.shape[0], original_for_cut.shape[1]), dtype=np.uint8)
    cv2.circle(mask_cv, (cx, cy), radius, (255), thickness=-1, lineType=cv2.LINE_AA) # Filled white circle

    # Crop bounding box of the circle first for efficiency
    x_crop_start = max(0, cx - lwidth) # Add some padding for line width
    y_crop_start = max(0, cy - lwidth)
    x_crop_end = min(original_for_cut.shape[1], cx + 2*radius + lwidth)
    y_crop_end = min(original_for_cut.shape[0], cy + 2*radius + lwidth)

    cropped_img_cv = original_for_cut[y_crop_start:y_crop_end, x_crop_start:x_crop_end]
    cropped_mask_cv = mask_cv[y_crop_start:y_crop_end, x_crop_start:x_crop_end]

    if cropped_img_cv.size == 0 or cropped_mask_cv.size == 0:
        print("Error: Cropped region or mask is empty.")
        return
        
    # Apply mask
    # Ensure mask is single channel for alpha
    if len(cropped_mask_cv.shape) == 3:
        cropped_mask_cv = cv2.cvtColor(cropped_mask_cv, cv2.COLOR_BGR2GRAY)

    # Split image into B, G, R, A channels
    b, g, r, a = cv2.split(cropped_img_cv)
    # Apply the mask to the alpha channel
    new_alpha = cv2.bitwise_and(a, a, mask=cropped_mask_cv)
    # Merge channels back
    result_cut_cv = cv2.merge((b, g, r, new_alpha))
    
    output_cut_path = os.path.join(cut_fig_dir, imgname[:-4] + '_cut_aa_cv2_' + cr + '.png')
    cv2.imwrite(output_cut_path, result_cut_cv)
    print(f"Saved anti-aliased cut image with CV2: {output_cut_path}")

def cut_picture(img, x, y, w, h, color=(0, 0, 255,255)):
    cut_img = img[y:y+h, x:x+w]
    # draw a bounding box at img
    cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
    # draw a bounding box at cut_img
    cv2.rectangle(cut_img, (0, 0), (w-1, h-1), color, 2)
    return img, cut_img

def sphere_cut(fig_dir, imgname, x,y,radius, lwidth, cr='red'):
    if cr == 'red':
        color = (255, 0, 0, 255)
    elif cr == 'green':
        color = (0, 255, 0, 255)
    elif cr == 'blue':
        color = (0, 0, 255, 255)
    elif cr == 'gray':
        color = (90, 90, 90, 255)
    else:
        print('Warning: Invalid color, use red instead.')
        color = (255, 0, 0, 255)
    # 798, 326, 153 head2
    img = os.path.join(fig_dir,imgname)
    cut_fig_dir = os.path.join(fig_dir, f'x{x}_y{y}_r{radius}_l{lwidth}/cut')
    bbx_fig_dir = os.path.join(fig_dir, f'x{x}_y{y}_r{radius}_l{lwidth}/bbx')
    os.path.exists(cut_fig_dir) or os.makedirs(cut_fig_dir)
    os.path.exists(bbx_fig_dir) or os.makedirs(bbx_fig_dir)
      
    # 以RGBA模式读取带有alpha通道的PNG图像  
    image = Image.open(img, 'r')  
      
    # 创建一个用于绘图的对象  
    draw = ImageDraw.Draw(image)  

    # 在图像指定位置画带有alpha通道的红色圆  
    draw.ellipse((x, y, x+2*radius, y+2*radius), outline=color, width=lwidth)  
      
    # 保存画了带有alpha通道的红色虚线圆的图片（保留透明度信息）  
   
    image.save(os.path.join(bbx_fig_dir,imgname[:-4]+'_sbbx_'+cr+'.png'))
      
     # 创建一个带有透明度通道的新图像  
    mask = Image.new("L", (2 * radius, 2 * radius), 0)
  
    # 创建一个用于绘图的对象  
    draw_mask = ImageDraw.Draw(mask)  
  
    # 在遮罩上画一个实心圆  
    draw_mask.ellipse((1, 1, 2 * radius-1, 2 * radius-1), width=lwidth, fill=1)
 
  
    # 裁剪圆包围的内容  
    cropped_image = image.crop((x, y, x + 2 * radius, y + 2 * radius))  
  
      
    result_image = ImageMath.eval("convert(a * b, 'L')", a=cropped_image.split()[3], b=mask) 
    
    # 将裁剪后的图片应用遮罩  
    cropped_image.putalpha(result_image)    
  
    # 保存裁剪后的图片（保留透明度信息）并画上圆  
    cropped_image.save(os.path.join(cut_fig_dir, imgname[:-4] + f'_{cr}.png'))
    print('朱志伟太帅了！！！')


def sphere_cut2(fig_dir, imgname, x, y, radius, lwidth, cr='red'):
    if cr == 'red':
        color = (255, 0, 0, 255)
    elif cr == 'green':
        color = (0, 255, 0, 255)
    elif cr == 'blue':
        color = (0, 0, 255, 255)
    elif cr == 'gray':
        color = (90, 90, 90, 255)
    else:
        print('Warning: Invalid color, use red instead.')
        color = (255, 0, 0, 255)
    # 798, 326, 153 head2
    img = os.path.join(fig_dir, imgname)
    cut_fig_dir = os.path.join(fig_dir, f'x{x}_y{y}_r{radius}_l{lwidth}/cut')
    bbx_fig_dir = os.path.join(fig_dir, f'x{x}_y{y}_r{radius}_l{lwidth}/bbx')
    os.path.exists(cut_fig_dir) or os.makedirs(cut_fig_dir)
    os.path.exists(bbx_fig_dir) or os.makedirs(bbx_fig_dir)

    # 以RGBA模式读取带有alpha通道的PNG图像
    image = Image.open(img, 'r')

    # 创建一个带有透明度通道的新图像
    mask = Image.new("L", (2 * radius, 2 * radius), 0)

    # 创建一个用于绘图的对象
    draw_mask = ImageDraw.Draw(mask)

    # 在遮罩上画一个实心圆
    draw_mask.ellipse((1, 1, 2 * radius - 1, 2 * radius - 1), width=1, fill=1)

    # 裁剪圆包围的内容
    cropped_image = image.crop((x, y, x + 2 * radius, y + 2 * radius))

    result_image = ImageMath.eval("convert(a * b, 'L')", a=cropped_image.split()[3], b=mask)

    # 将裁剪后的图片应用遮罩
    cropped_image.putalpha(result_image)

    # 保存裁剪后的图片（保留透明度信息）,没有圆
    cropped_image.save(os.path.join(cut_fig_dir, imgname[:-4] + '_cut2_' + cr + '.png'))

    # 创建一个用于绘图的对象
    draw = ImageDraw.Draw(image)

    # 在图像指定位置画带有alpha通道的红色圆
    draw.ellipse((x, y, x + 2 * radius, y + 2 * radius), outline=color, width=lwidth)

    # 保存画了带有alpha通道的红色虚线圆的图片（保留透明度信息）

    image.save(os.path.join(bbx_fig_dir, imgname[:-4] + '_sbbx2_' + cr + '.png'))


    print('朱志伟太帅了！！！')

def read_cut():
    fig_dir = '/work/Users/zhuzhiwei/tools/BlenderToolbox/fig/horse14'
    cut_fig_dir = os.path.join(fig_dir, 'cut')
    bbx_fig_dir = os.path.join(fig_dir, 'bbx')
    os.path.exists(cut_fig_dir) or os.makedirs(cut_fig_dir)
    os.path.exists(bbx_fig_dir) or os.makedirs(bbx_fig_dir)
    mat = 'yellow'
    #mat = 'balloon'
    #mat = 'edge'
    # len(list_horse14) =5
    name_dog7 = ['loop', 'butterfly', 'mod_butterfly', 'neuralSubdiv', 'midpoint']
    for i in range(1):
        name = name_horse14[i]
        name = 'ns_horse14_subd3'
        imgPath = os.path.join(fig_dir, name + '_' + mat + '_1920_300.png')
        bbx_imgPath = os.path.join(bbx_fig_dir, name + '_' + mat + '_1920_300_bbx.png')

        print(imgPath)
        img = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)
        # cut 1 900, 366, 150, 150 - 1350, 549, 225, 225
        cut1_path = os.path.join(cut_fig_dir, name + '_' + mat + '_1920_300_cut1.png')
        img, cut1_img = cut_picture(img, 1350, 549, 225, 225)

        # cut 2 520, 500, 150, 150 - 780, 750, 225, 225
        cut2_path = os.path.join(cut_fig_dir, name + '_' + mat + '_1920_300_cut2.png')
        img, cut2_img = cut_picture(img, 780, 750, 225, 225, (255, 0, 0, 255))

        cv2.imwrite(cut1_path, cut1_img)
        cv2.imwrite(cut2_path, cut2_img)
        cv2.imwrite(bbx_imgPath, img)
'''
    name = name_horse14[i]
    name = 'horse14_subd3'
    imgPath = os.path.join(fig_dir, name+'_' + mat + '_1920_300.png')
    bbx_imgPath = os.path.join(bbx_fig_dir, name+'_' + mat + '_1920_300_bbx.png')

    print(imgPath)
    img = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)
    # cut 1 900, 366, 150, 150 - 1350, 549, 225, 225
    cut1_path = os.path.join(cut_fig_dir, name+'_' + mat + '_1920_300_cut1.png')
    img, cut1_img = cut_picture(img, 1350, 549, 225, 225)

    # cut 2 520, 500, 150, 150 - 780, 750, 225, 225
    cut2_path = os.path.join(cut_fig_dir, name + '_' + mat + '_1920_300_cut2.png')
    img, cut2_img = cut_picture(img, 780, 750, 225, 225, (255,0,0,255))
dog7
    img, cut1_img = cut_picture(img, 700, 320, 100 , 100)
    img, cut2_img = cut_picture(img, 560, 780, 100 , 100, (255,0,0,255))

spot_body2
    600 970 240 240 
'''
if __name__ == '__main__':
    fig_dir = '/work/Users/zhuzhiwei/project/6figure/BlenderToolbox/fig/bob/owl_fish/'
    imgname = 'ours_bob_owl_subd2_balloon.png'  # ns_bob_owl_subd2_yellow.png  ours_bob_owl_subd2_balloon
    #read_cut()
    # 794, 322, 153 head2
    # 590, 935, 135 body2
    # 500, 440, 180 cactus
    # 670, 440, 90 cactus small
    # 335, 590, 75 1093600
    # 450, 590, 60 owl
    sphere_cut(fig_dir, imgname, 450, 550, 80, 4, cr='gray')
    
