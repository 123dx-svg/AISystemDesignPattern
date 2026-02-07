# AI Design Patterns 演示项目

本项目演示了 5 种常用的 AI 应用设计模式，使用 Jupyter Notebooks 进行交互式展示。

## 📚 包含的设计模式

1. **Prompt Chaining** (提示链) - 将复杂任务分解为顺序执行的步骤
2. **Routing** (路由) - 根据输入智能选择最合适的处理路径
3. **Parallelization** (并行化) - 多个 LLM 并行执行以提高效率
4. **Orchestrator-Worker** (编排器-工作器) - 协调多个专业化的 AI 工作器
5. **Evaluator-Optimizer** (评估-优化器) - 自动评估和优化输出质量

## 🚀 快速开始

### 前置要求
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) 包管理器
- Visual Studio Code (推荐)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/123dx-svg/AISystemDesignPattern.git
   cd AISystemDesignPattern
   ```

2. **安装依赖**
   ```bash
   uv sync
   ```

3. **配置 API 密钥**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，添加您的 OpenRouter API 密钥
   ```

4. **安装 Jupyter Kernel**
   ```bash
   # Windows
   .venv\Scripts\python -m ipykernel install --user --name=ainew --display-name="Python (AISystemDesignPattern)"

   # macOS/Linux
   .venv/bin/python -m ipykernel install --user --name=ainew --display-name="Python (AISystemDesignPattern)"
   ```

5. **在 VSCode 中打开项目**
   - 打开任意 `.ipynb` 文件
   - 选择 "Python (AINew)" kernel
   - 开始运行！

## 📖 详细文档

查看 [DEPLOYMENT.md](DEPLOYMENT.md) 了解完整的部署指南和故障排除。

## 🛠️ 技术栈

- **AI/LLM**: OpenRouter, Anthropic Claude, OpenAI GPT
- **数据处理**: NumPy, Pandas
- **可视化**: Matplotlib, Plotly
- **框架**: LangChain, LangGraph, AutoGen
- **开发工具**: Jupyter, IPython

## 📁 项目结构

```
AINew/
├── .env.example              # 环境变量模板
├── .gitignore               # Git 忽略规则
├── pyproject.toml           # 项目配置和依赖
├── uv.lock                  # 锁定的依赖版本
├── requirements.txt         # 依赖列表（备用）
├── DEPLOYMENT.md            # 详细部署指南
├── README.md                # 项目说明
├── AI-Design-Patterns-Summary.ipynb  # 5种模式对比总结
├── PromptChaining.ipynb     # 提示链模式
├── Routing.ipynb            # 路由模式
├── Parallelization.ipynb    # 并行化模式
├── Orchestrator-Worker.ipynb # 编排器-工作器模式
└── Evaluate-Optimizer.ipynb  # 评估-优化器模式
```

## 🔑 API 密钥配置

获取 OpenRouter API 密钥：https://openrouter.ai/keys

在 `.env` 文件中配置：
```
OPENROUTER_API_KEY=your_key_here
```

## 📊 运行示例

每个 Notebook 都包含完整的代码示例和详细说明。建议按以下顺序学习：

1. `PromptChaining.ipynb` - 最简单的模式，适合入门
2. `Routing.ipynb` - 学习条件分支
3. `Parallelization.ipynb` - 理解并行执行
4. `Orchestrator-Worker.ipynb` - 掌握任务编排
5. `Evaluate-Optimizer.ipynb` - 学习质量优化
6. `AI-Design-Patterns-Summary.ipynb` - 查看完整对比

## 🤝 贡献

欢迎提交 Issues 和 Pull Requests！

## 📄 许可

MIT License

## 🙏 致谢

本项目基于 AI 应用开发最佳实践，参考了多个开源项目和社区贡献。

---

**祝您学习愉快！如有问题，请查看 [DEPLOYMENT.md](DEPLOYMENT.md) 或提交 Issue。**
