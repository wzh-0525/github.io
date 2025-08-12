# 查询网格分析工具

这是一个用于分析查询数据中领域与意图交叉分布的可视化工具，支持一级和二级领域/意图的切换分析。

## 功能特点

- 📊 **交互式网格热力图**：直观显示领域与意图的交叉分布
- 🔄 **级别切换**：支持一级/二级领域和意图的动态切换
- 🎨 **蓝色渐变配色**：数值越大颜色越深，视觉效果清晰
- 📁 **Excel文件支持**：直接上传Excel文件进行分析
- 📈 **统计信息**：显示总查询数、领域数量、意图数量等统计数据
- 💾 **数据导出**：支持CSV格式导出分析结果
- 🖱️ **交互功能**：点击网格查看详细信息，鼠标悬停显示提示

## 文件说明

### 1. query_grid_analysis.html
**Web版可视化工具**
- 基于HTML/CSS/JavaScript开发
- 支持Excel文件上传和在线分析
- 包含示例数据，可直接体验
- 响应式设计，支持移动端

**使用方法：**
```bash
# 直接在浏览器中打开
open query_grid_analysis.html
```

### 2. grid_analyzer.py
**Python版分析工具**
- 基于pandas、matplotlib、seaborn开发
- 支持批量生成所有组合的热力图
- 自动导出CSV文件和PNG图片
- 提供详细的统计信息

**使用方法：**
```bash
# 使用Excel文件
python3 grid_analyzer.py AI_search_log_query_domain_update.xlsx

# 使用示例数据
python3 grid_analyzer.py
```

## 数据格式要求

Excel文件应包含以下列：
- `First_domain`: 一级领域
- `Second_Domain`: 二级领域  
- `First_Intent`: 一级意图
- `Second_Intent`: 二级意图
- `query`: 查询内容（可选）

## 安装依赖

### Python依赖
```bash
pip3 install pandas openpyxl xlrd matplotlib seaborn
```

### Web版本
无需安装，直接在浏览器中打开HTML文件即可。

## 使用示例

### 1. Web版本使用
1. 在浏览器中打开 `query_grid_analysis.html`
2. 点击"加载示例数据"查看效果，或上传Excel文件
3. 使用控制按钮切换领域和意图级别
4. 点击网格单元格查看详细信息
5. 使用"导出数据"按钮下载CSV文件

### 2. Python版本使用
```python
from grid_analyzer import QueryGridAnalyzer

# 创建分析器
analyzer = QueryGridAnalyzer('your_data.xlsx')

# 生成热力图
analyzer.plot_heatmap('first', 'first')  # 一级领域 vs 一级意图

# 查看统计信息
analyzer.print_statistics('first', 'first')

# 生成所有组合的图表
analyzer.generate_all_combinations()
```

## 输出文件

Python版本会生成以下文件：
- `output/一级领域_vs_一级意图.png`
- `output/一级领域_vs_二级意图.png`
- `output/二级领域_vs_一级意图.png`
- `output/二级领域_vs_二级意图.png`
- `query_grid_first_first.csv`
- `query_grid_first_second.csv`
- `query_grid_second_first.csv`
- `query_grid_second_second.csv`

## 特性说明

### 颜色映射
- 使用蓝色渐变色系
- 从浅蓝色（#f8f9fa）到深蓝色（#0d47a1）
- 数值为0时显示灰白色
- 数值越大颜色越深

### 交互功能
- **鼠标悬停**：显示详细信息提示
- **点击单元格**：弹出详细查询列表
- **级别切换**：动态切换一级/二级分析
- **数据导出**：一键导出分析结果

### 统计信息
- 总查询数量
- 领域数量
- 意图数量
- 最大计数值
- 平均值和标准差

## 技术栈

### Web版本
- HTML5 + CSS3
- JavaScript (ES6+)
- SheetJS (Excel文件解析)

### Python版本
- pandas (数据处理)
- matplotlib (图表绘制)
- seaborn (热力图)
- numpy (数值计算)

## 浏览器兼容性

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 注意事项

1. Excel文件编码建议使用UTF-8
2. 数据量过大时建议使用Python版本
3. Web版本在移动端可能显示效果有限
4. 确保数据列名与要求格式一致

## 常见问题

**Q: 上传Excel文件后显示错误？**
A: 请检查文件格式和列名是否正确，确保包含必要的列。

**Q: 热力图显示不完整？**
A: 可能是数据量过大，建议调整浏览器窗口大小或使用Python版本。

**Q: 中文显示乱码？**
A: 确保Excel文件使用UTF-8编码保存。

## 更新日志

- v1.0.0: 初始版本，支持基本的网格分析功能
- 支持一级/二级领域和意图切换
- 实现蓝色渐变热力图
- 添加交互功能和数据导出

## 许可证

MIT License
