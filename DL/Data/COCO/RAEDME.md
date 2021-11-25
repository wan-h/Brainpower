## COCO
[Link](https://cocodataset.org/)

---
### DESCRIPTION
COCO数据比较大，数据集的所有信息都存储到一个json文件中  
其json内容如下  
```
{
  "info": {
    "description": "COCO 2017 Dataset",
    "url": "http://cocodataset.org",
    "version": "1.0",
    "year": 2017,
    "contributor": "COCO Consortium",
    "date_created": "2017/09/01"
  },
  "licenses": [
    {
      "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
      "id": 1,
      "name": "Attribution-NonCommercial-ShareAlike License"
    },
    ...
  ]
  "images": [
    {
      "license": 4,
      "file_name": "000000397133.jpg",
      "coco_url": "http://images.cocodataset.org/val2017/000000397133.jpg",
      "height": 427,
      "width": 640,
      "date_captured": "2013-11-14 17:02:52",
      "flickr_url": "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",
      "id": 397133
    },
    ...
  ]
  # 标注信息
  "annotations": [
    {
      "segmentation": [
        [
          510.66,
          423.01,
          ...
        ]
      ],
      "area": 702.1057499999998,
      # 0表示单个对象，分割使用polygon表示；1表示一组对象，分割使用RLE格式表示
      "iscrowd": 0,
      "image_id": 289343,
      "bbox": [
        473.07,
        395.93,
        38.65,
        28.67
      ],
      # 类别id，对应最后的类别列表
      "category_id": 18,
      "id": 1768
    },
    ...
  ]
  "categories": [
    {
      # 父类
      "supercategory": "person",
      "id": 1,
      # 当前类别
      "name": "person"
    },
    {
      "supercategory": "vehicle",
      "id": 2,
      "name": "bicycle"
    },
    {
      "supercategory": "vehicle",
      "id": 3,
      "name": "car"
    },
    ...
  ]
}
```