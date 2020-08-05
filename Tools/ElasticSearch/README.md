## ElasticSearch
[Link](https://www.elastic.co/cn/elasticsearch/)  

---
### OVERVIEW  
Elasticsearch 是一个分布式、RESTful 风格的搜索和数据分析引擎。
通过 Elasticsearch，您能够分析大规模数据并执行合并多种类型的搜索（结构化数据、非结构化数据、地理位置、指标）。

### 基本概念
* 倒排索引（Inverted Index）  
该索引表中的每一项都包括一个属性值和具有该属性值的各记录的地址。由于不是由记录来确定属性值，而是由属性值来确定记录的位置，
因而称为倒排索引(inverted index)。Elasticsearch能够实现快速、高效的搜索功能，正是基于倒排索引原理。  

* 节点 & 集群（Node & Cluster）  
Elasticsearch 本质上是一个分布式数据库，允许多台服务器协同工作，每台服务器可以运行多个Elasticsearch实例。
单个Elasticsearch实例称为一个节点（Node），一组节点构成一个集群（Cluster）。  

* 索引（Index）  
Elasticsearch 数据管理的顶层单位就叫做 Index（索引），相当于关系型数据库里的数据库的概念。另外，每个Index的名字必须是小写。  

* 类型（Type）  
Document 可以分组，比如employee这个 Index 里面，可以按部门分组，也可以按职级分组。这种分组就叫做 Type，它是虚拟的逻辑分组，
用来过滤 Document，类似关系型数据库中的数据表。不同的 Type 应该有相似的结构（Schema），性质完全不同的数据（比如 products 和 logs）应该存成两个 Index，
而不是一个 Index 里面的两个 Type（虽然可以做到）。  

* 文档（Document）
Index里面单条的记录称为 Document（文档）。许多条 Document 构成了一个 Index。Document 使用 JSON 格式表示。
同一个 Index 里面的 Document，不要求有相同的结构（scheme），但是最好保持相同，这样有利于提高搜索效率。  

* 文档元数据（Document metadata）  
文档元数据为_index, _type, _id, 这三者可以唯一表示一个文档，_index表示文档在哪存放，_type表示文档的对象类别，_id为文档的唯一标识。  

* 字段（Fields）  
每个Document都类似一个JSON结构，它包含了许多字段，每个字段都有其对应的值，多个字段组成了一个 Document，可以类比关系型数据库数据表中的字段。
在 Elasticsearch 中，文档（Document）归属于一种类型（Type），而这些类型存在于索引（Index）中，下图展示了Elasticsearch与传统关系型数据库的类比：  
![](src/Oth_0.png)

### Kibana  
[Link](https://www.elastic.co/kibana)  
Kibana将Elasticsearch视为存储和处理数据的引擎，然后构建漂亮的可视化效果和仪表板。