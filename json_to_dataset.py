import argparse
import base64
import json
import os
import os.path as osp
import yaml
import imgviz
import PIL.Image
from os import listdir
from os.path import isfile, isdir, join
from labelme.logger import logger
from labelme import utils
def main():
    logger.warning(
        "It can handle multiple JSON files to generate a "
        "real-use dataset."
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file")
    parser.add_argument("-o", "--out", default=None)
    args = parser.parse_args()
    nowpath = args.json_file
    if args.out is None:
        out_dir = osp.basename(json_file).replace(".", "_")
        out_dir = osp.join(osp.dirname(json_file), out_dir)
    else:
        out_dir = args.out
    cv2_mask=osp.join(out_dir,"cv2_mask")
    pic=osp.join(out_dir,"pic")
    jsonpath=osp.join(out_dir,"json")
    if not osp.exists(cv2_mask):
        os.mkdir(cv2_mask)
    if not osp.exists(pic):
        os.mkdir(pic)
    if not osp.exists(jsonpath):
        os.mkdir(jsonpath)
    if not osp.exists(out_dir):
        os.mkdir(out_dir)
    out_dir=osp.join(out_dir,"labelme_json")
    if not osp.exists(out_dir):
        os.mkdir(out_dir)
    files = listdir(nowpath)
    i=1
    for f in files:
        if(f[-4:]=="json"):
                subout_dir=osp.join(out_dir,str(i)+"_json")
                if not osp.exists(subout_dir):
                    os.mkdir(subout_dir)
                data = json.load(open(osp.join(nowpath,f),encoding="utf-8"))
                imageData = data.get("imageData")
                if not imageData:
                    imagePath = os.path.join(os.path.dirname(f),data["imagePath"])
                    with open(imagePath, "rb") as f:
                        imageData = f.read()
                        imageData = base64.b64encode(imageData).decode("utf-8")
                img = utils.img_b64_to_arr(imageData)
                label_name_to_value = {"_background_": 0}
                for shape in sorted(data["shapes"], key=lambda x: x["label"]):
                    label_name = shape["label"]
                    if label_name in label_name_to_value:
                        label_value = label_name_to_value[label_name]
                    else:
                        label_value = len(label_name_to_value)
                        label_name_to_value[label_name] = label_value
                lbl, _ = utils.shapes_to_label(
                    img.shape, data["shapes"], label_name_to_value
                )
                label_names = [None] * (max(label_name_to_value.values()) + 1)
                for name, value in label_name_to_value.items():
                    label_names[value] = name
                lbl_viz = imgviz.label2rgb(
                    lbl, imgviz.asgray(img), label_names=label_names, loc="rb"
                )
                PIL.Image.fromarray(img).save(osp.join(subout_dir, "img.png"))
                PIL.Image.fromarray(img).save(osp.join(pic,str(i)+".png"))
                utils.lblsave(osp.join(subout_dir, "label.png"), lbl)
                utils.lblsave(osp.join(cv2_mask,str(i)+".png"), lbl)
                PIL.Image.fromarray(lbl_viz).save(osp.join(subout_dir, "label_viz.png"))
                with open(osp.join(jsonpath,str(i)+".json"), 'w') as jsonfile:
                    json.dump(data, jsonfile)
                with open(osp.join(subout_dir, "label_names.txt"), "w") as f:
                    for lbl_name in label_names:
                        f.write(lbl_name + "\n")
                logger.warning('info.yaml is being replaced by label_names.txt')
                info = dict(label_names=label_names)
                with open(osp.join(subout_dir, 'info.yaml'), 'w') as f:
                    yaml.safe_dump(info, f, default_flow_style=False)
                logger.info("Saved to: {}".format(subout_dir))
                i+=1
if __name__ == "__main__":
    main()
