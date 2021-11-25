## Pascal VOC
[Link](https://pjreddie.com/projects/pascal-voc-dataset-mirror/)

---
### DESCRIPTION
* 目录结构  
.  
├── Annotations #存放标注文件(.xml)  
├── ImageSets #存放不同图片集  
│   ├── Action #存放动作相关数据集合(.txt)  
│   ├── Layout #存放人体部位相关数据集合(.txt)  
│   ├── Main #存档目标检测相关数据集合(.txt)  
│   └── Segmentation #存放语义分割数据集合(.txt)  
├── JPEGImages #存放源图片(.jpg)  
├── SegmentationClass #存放语义分割图片(.png)  
└── SegmentationObject #存放目标分割图片(.png)  
* 文件解析  

Annotations中的标注文件  
```
<annotation>
	<folder>VOC2012</folder>  #表明图片来源
	<filename>2007_000027.jpg</filename> #图片名称
	<source>                  #图片来源相关信息
		<database>The VOC2007 Database</database>
		<annotation>PASCAL VOC2007</annotation>
		<image>flickr</image>
	</source>
	<size>     #图像尺寸
		<width>486</width>
		<height>500</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented> #是否用于分割
	<object>  #包含的物体
		<name>person</name> #物体类别
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>  #物体的bbox
			<xmin>174</xmin>
			<ymin>101</ymin>
			<xmax>349</xmax>
			<ymax>351</ymax>
		</bndbox>
		<part> #物体的头
			<name>head</name>
			<bndbox>
				<xmin>169</xmin>
				<ymin>104</ymin>
				<xmax>209</xmax>
				<ymax>146</ymax>
			</bndbox>
		</part>
		<part>   #物体的手
			<name>hand</name>
			<bndbox>
				<xmin>278</xmin>
				<ymin>210</ymin>
				<xmax>297</xmax>
				<ymax>233</ymax>
			</bndbox>
		</part>
		<part>
			<name>foot</name>
			<bndbox>
				<xmin>273</xmin>
				<ymin>333</ymin>
				<xmax>297</xmax>
				<ymax>354</ymax>
			</bndbox>
		</part>
		<part>
			<name>foot</name>
			<bndbox>
				<xmin>319</xmin>
				<ymin>307</ymin>
				<xmax>340</xmax>
				<ymax>326</ymax>
			</bndbox>
		</part>
	</object>
</annotation>
```  

ImageSets下的图片集合文件  
train后缀代表训练集，val代表验证集合，trainval代表融合训练验证，test代表测试集  
```
Action 第一个数字表示图中包含的人数，第二个数字表示图中人的动作状态是否满足  
2011_003279 1 1  
  
Layout 第一个数字表示图中包含的人数  
2011_003279 1  
  
Main 类别数据集第一个数子代表是否属于该类  
2011_003279 -1  
  
Segmentation 直接表示对应的图片文件名称  
2011_003279  
```

JPEGImages下直接存储和ImageSets文件中名字标志对应的图片源数据    
SegmentationClass下存储按照各类别的分割图片，其中颜色和类别的对应关系可以参照网络上的解析    
SegmentationObject下存储按照各对象的分割图片  
