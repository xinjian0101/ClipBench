# ClipBench

短视频高光片段算法的区间评测工具。

## MVP

- 计算区间 IoU
- 输出 Precision、Recall、F1
- 统计平均边界误差
- 支持 JSON 真值与预测结果

## 运行

```bash
python main.py examples/truth.json examples/predicted.json --threshold 0.5 -o report.json
```

## 测试

```bash
python -m unittest -v
```

## License

MIT
