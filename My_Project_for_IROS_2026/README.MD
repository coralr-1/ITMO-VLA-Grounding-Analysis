# 🤖 AI-Powered Shadow Hand ASL Control System
# 🤖 AI驱动的Shadow Hand手语控制系统

[English](#english) | [中文](#chinese)

---

<a name="english"></a>

## 📖 English Version

### 🎯 Project Overview

An intelligent robotic hand control system that **listens to your voice**, **corrects speech recognition errors**, **translates Chinese to English**, and controls a simulated Shadow Hand to perform American Sign Language (ASL) finger-spelling gestures.

**🎥 Demo Video**: [LLM_robots.mp4](../)

### ✨ Key Features

- 🎤 **Voice Recognition**: Real-time Chinese speech input via Google Speech API
- 🧠 **AI Error Correction**: Local LLM automatically fixes homophones and typos (e.g., "怎么周" → "怎么走")
- 🌐 **Translation**: Chinese → English translation with letter sequence generation
- 🤖 **Closed-Loop Control**: Smooth motion with joint position feedback (no glitchy movements)
- 🔤 **Complete ASL Alphabet**: A-Z gesture support using Shadow Hand simulation
- 💻 **PyBullet Physics**: Realistic robotic hand simulation with gravity and collision

---

### 🏗️ System Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Voice     │──────│     LLM      │──────│   Shadow    │
│  (Chinese)  │ ASR  │  (Correct +  │ JSON │    Hand     │
│  Microphone │      │   Translate) │      │ (PyBullet)  │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                     ┌──────┴──────┐
                     │ LM Studio   │
                     │ Local API   │
                     │ Port: 1234  │
                     └─────────────┘
```

**Workflow**:
1. User speaks in Chinese via microphone
2. Google Speech API transcribes to text (may contain errors)
3. Local LLM corrects errors & translates to English
4. System converts to letter sequence: `["H","E","L","L","O"]`
5. Shadow Hand executes ASL gestures sequentially

---

### 📋 Prerequisites

| Requirement | Specification |
|------------|---------------|
| **OS** | Windows 10/11, Linux (Ubuntu 20.04+) |
| **Python** | 3.10 or higher |
| **LLM Server** | [LM Studio](https://lmstudio.ai/) (for local inference) |
| **Hardware** | Microphone (required), Internet connection (for Google ASR) |
| **GPU** | Optional (improves rendering quality) |

---

### 🚀 Installation

#### Step 1: Clone/Download Project

Ensure these files are in the **same directory**:
```
asl_robot_project/
├── asl_main.py              # Main control script
├── my_shadow_hand.urdf      # Shadow Hand robot model
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

#### Step 2: Install Python Dependencies

**Windows:**
```bash
pip install -r requirements.txt

# If pyaudio fails, use:
pip install pipwin
pipwin install pyaudio
```

**Linux (Ubuntu):**
```bash
# Install system-level audio libraries
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev

# Install Python packages
pip install -r requirements.txt
```

#### Step 3: Setup LM Studio (LLM Server)

1. Download and install [LM Studio](https://lmstudio.ai/)
2. Open LM Studio and download a model:
   - **Recommended**: `Qwen2.5-1.5B-Instruct` (fast) or `Qwen2.5-7B-Instruct` (more accurate)
3. Click **Local Server** (icon with bidirectional arrows) in the left sidebar
4. Click green **Start Server** button at the top
5. Verify the console shows: `Server running at http://localhost:1234`

---

### 🎮 Usage

#### Starting the System

```bash
python asl_main.py
```

**Expected output:**
```
正在启动 PyBullet...
=== Shadow Hand 智能控制系统 ===
操作指南: 按 'v' 键说话，按 'q' 退出

输入指令 (v=语音, q=退出):
```

#### Operation Modes

**Mode A: Voice Control (Recommended ✨)**

1. Type `v` and press Enter
2. Wait for: `🎤 正在调整环境噪音...` (stay silent for 1 second)
3. When you see `🔴 请说话! (Listening...)`, speak in Chinese
   - Example: *"你好我想去学校"* (Hello, I want to go to school)
4. The system will:
   - Recognize speech → Correct errors → Translate → Execute ASL gestures

**Example Output:**
```
👂 听到: 【 你好怎么周 】
🧠 发送给大脑纠错: 你好怎么周 ...
✨ 智能纠错: 你好怎么走
📖 翻译结果: HELLO HOW TO GO
准备执行序列: ['H', 'E', 'L', 'L', 'O', ' ', 'H', 'O', 'W', ...]
>>> 动作: H
>>> 动作: E
...
```

**Mode B: Text Input (Debugging)**

1. Directly type Chinese or English text at the prompt
   - Example: `Hello World` or `你好`
2. Press Enter to execute gestures

**Exiting:**
- Type `q` and press Enter

---

### 🧪 Demo Scenarios

Test the system's intelligence with challenging inputs:

#### Test 1: Homophone Correction
- **Input (voice)**: "我想去**碎觉**" (shuì jiào - intentional typo)
- **System Output**:
  ```
  ✨ 智能纠错: 我想去睡觉
  📖 翻译: I WANT TO SLEEP
  ```
- **Action**: Spells `S-L-E-E-P`

#### Test 2: Long Sentence Translation
- **Input (voice)**: "机器人技术非常有趣"
- **System Output**:
  ```
  📖 翻译: ROBOTICS IS VERY INTERESTING
  ```
- **Action**: Spells entire sentence

---

### 🔧 Configuration

#### API Endpoint (Line 10 in `asl_main.py`)
```python
API_URL = "http://localhost:1234/v1/chat/completions"
```
- Default port is `1234` (LM Studio default)
- Change if using different LLM server

#### Graphics Mode (Line 33 in `asl_main.py`)
```python
# Current (compatibility mode):
p.connect(p.GUI, options="--opengl2")

# High-performance mode (requires good GPU):
p.connect(p.GUI)
```
- Remove `options="--opengl2"` for better graphics if you have NVIDIA GPU
- Revert if you experience crashes

---

### 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: speech_recognition` | Run: `pip install SpeechRecognition` |
| Voice recognition timeout | 1. Check internet connection<br>2. Ensure microphone is not muted<br>3. Speak louder and slower |
| `Connection Error` to LLM | Verify LM Studio server is running on port 1234 |
| Hand moves too slowly | **Normal behavior** - closed-loop control ensures smooth motion |
| URDF loading error | Verify `my_shadow_hand.urdf` is in same directory as script |
| PyBullet crashes | Add `options="--opengl2"` to `p.connect()` line |

---

### 📂 Project Structure

```
asl_robot_project/
├── asl_main.py              # Main control script (250 lines)
│   ├── Voice Recognition    # Google Speech API integration
│   ├── LLM Interface        # Local LLM API calls
│   ├── ASL Pose Library     # A-Z gesture definitions
│   ├── Closed-Loop Control  # Joint position feedback
│   └── PyBullet Simulation  # Physics engine
│
├── my_shadow_hand.urdf      # Robot model definition
│   ├── 20 movable joints    # Fingers + wrist
│   └── Collision meshes     # For physics
│
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

---

### 🎨 Technical Highlights

1. **Intelligent Error Correction**
   - Uses LLM to fix ASR mistakes contextually
   - Handles homophones: "怎么周" → "怎么走"

2. **Closed-Loop Motion Control**
   ```python
   # Waits until joint reaches target ±0.15 radians
   while time.time() - start < 2.0:
       curr = p.getJointState(robot_id, joint_id)[0]
       if abs(curr - target) < 0.15:
           break
   ```

3. **ASL Gesture Library**
   - 26 letters + REST pose
   - Finger abbreviations: FF (forefinger), MF (middle), RF (ring), LF (little), TH (thumb)
   - Example A: All fingers bent, thumb slightly abducted

4. **Noise Cancellation**
   ```python
   r.adjust_for_ambient_noise(source, duration=0.8)
   r.pause_threshold = 1.5  # Prevents cutting off speech
   ```

---

### 📊 System Performance

| Metric | Value |
|--------|-------|
| ASR Latency | ~2-3 seconds (Google API) |
| LLM Inference | ~1-2 seconds (Qwen2.5-1.5B on CPU) |
| Gesture Execution | ~1-2 seconds per letter |
| Joint Precision | ±0.15 radians |
| Physics Timestep | 240 Hz (PyBullet) |

---

### 🔮 Future Improvements

- [ ] Add dynamic ASL gestures (not just finger-spelling)
- [ ] Support offline ASR (Whisper integration)
- [ ] Multi-hand coordination for complex phrases
- [ ] Real robot deployment (UR5 + Leap Hand)
- [ ] Web interface for remote control

---

### 📄 License

MIT License - Feel free to use for educational/research purposes.

---

### 🙏 Acknowledgments

- **Shadow Hand Model**: Based on OpenAI Shadow Hand URDF
- **LLM**: Powered by Qwen2.5 (Alibaba Cloud)
- **Physics Engine**: PyBullet
- **Speech Recognition**: Google Cloud Speech-to-Text

---

<a name="chinese"></a>

## 📖 中文版本

### 🎯 项目概述

这是一个智能机械手控制系统，能够**听懂你的声音**、**自动纠正识别错误**、**翻译成英文**，并控制仿真Shadow Hand执行美式手语(ASL)字母拼写手势。

**🎥 演示视频**: [LLM_robots.mp4](../LLM_robots.mp4)

### ✨ 核心功能

- 🎤 **语音识别**: 通过Google语音API实时输入中文
- 🧠 **AI智能纠错**: 本地大模型自动修复同音错别字（如"怎么周"→"怎么走"）
- 🌐 **翻译功能**: 中文→英文翻译并生成字母序列
- 🤖 **闭环控制**: 平滑运动，带关节位置反馈（杜绝鬼畜动作）
- 🔤 **完整ASL字母表**: 支持A-Z所有手语字母
- 💻 **PyBullet物理仿真**: 真实的机械手仿真，带重力和碰撞

---

### 🏗️ 系统架构

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   语音输入   │──────│   大语言模型  │──────│  Shadow Hand │
│  (中文)     │ 识别  │  (纠错+翻译)  │ JSON │  (PyBullet)  │
│   麦克风    │      │              │      │   仿真手     │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                     ┌──────┴──────┐
                     │  LM Studio  │
                     │  本地API服务 │
                     │  端口: 1234 │
                     └─────────────┘
```

**工作流程**:
1. 用户对麦克风说中文
2. Google语音API转文字（可能有错误）
3. 本地LLM纠错并翻译成英文
4. 系统转换为字母序列: `["H","E","L","L","O"]`
5. Shadow Hand依次执行ASL手势

---

### 📋 环境要求

| 需求项 | 规格 |
|-------|------|
| **操作系统** | Windows 10/11, Linux (Ubuntu 20.04+) |
| **Python版本** | 3.10 或更高 |
| **LLM服务器** | [LM Studio](https://lmstudio.ai/) (本地推理) |
| **硬件** | 麦克风（必需）、互联网连接（用于Google ASR） |
| **显卡** | 可选（提升渲染质量） |

---

### 🚀 安装步骤

#### 第一步：准备项目文件

确保以下文件在**同一目录**下:
```
asl_robot_project/
├── asl_main.py              # 主控制脚本
├── my_shadow_hand.urdf      # Shadow Hand机器人模型
├── requirements.txt         # Python依赖列表
└── README.md                # 本文档
```

#### 第二步：安装Python依赖

**Windows系统:**
```bash
pip install -r requirements.txt

# 如果pyaudio安装失败，使用:
pip install pipwin
pipwin install pyaudio
```

**Linux系统 (Ubuntu):**
```bash
# 安装系统级音频库
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev

# 安装Python包
pip install -r requirements.txt
```

#### 第三步：配置LM Studio（大模型服务器）

1. 下载并安装 [LM Studio](https://lmstudio.ai/)
2. 打开LM Studio并下载模型：
   - **推荐**: `Qwen2.5-1.5B-Instruct`（速度快）或 `Qwen2.5-7B-Instruct`（更准确）
3. 点击左侧栏的 **Local Server**（双向箭头图标）
4. 点击顶部绿色 **Start Server** 按钮
5. 确认控制台显示: `Server running at http://localhost:1234`

---

### 🎮 使用方法

#### 启动系统

```bash
python asl_main.py
```

**预期输出:**
```
正在启动 PyBullet...
=== Shadow Hand 智能控制系统 ===
操作指南: 按 'v' 键说话，按 'q' 退出

输入指令 (v=语音, q=退出):
```

#### 操作模式

**模式A：语音控制（推荐 ✨）**

1. 输入 `v` 并按回车
2. 等待提示: `🎤 正在调整环境噪音...`（保持安静1秒）
3. 看到 `🔴 请说话! (Listening...)`时，对着麦克风说中文
   - 示例: *"你好我想去学校"*
4. 系统将：
   - 识别语音 → 纠正错误 → 翻译 → 执行ASL手势

**示例输出:**
```
👂 听到: 【 你好怎么周 】
🧠 发送给大脑纠错: 你好怎么周 ...
✨ 智能纠错: 你好怎么走
📖 翻译结果: HELLO HOW TO GO
准备执行序列: ['H', 'E', 'L', 'L', 'O', ' ', 'H', 'O', 'W', ...]
>>> 动作: H
>>> 动作: E
...
```

**模式B：文字输入（调试用）**

1. 直接在提示符下输入中文或英文
   - 示例: `Hello World` 或 `你好`
2. 按回车执行手势

**退出程序:**
- 输入 `q` 并按回车

---

### 🧪 测试场景

用挑战性输入测试系统智能程度：

#### 测试1：同音字纠正
- **语音输入**: "我想去**碎觉**"（故意错误）
- **系统输出**:
  ```
  ✨ 智能纠错: 我想去睡觉
  📖 翻译: I WANT TO SLEEP
  ```
- **动作**: 拼写 `S-L-E-E-P`

#### 测试2：长句翻译
- **语音输入**: "机器人技术非常有趣"
- **系统输出**:
  ```
  📖 翻译: ROBOTICS IS VERY INTERESTING
  ```
- **动作**: 拼写完整句子

---

### 🔧 配置说明

#### API端点（`asl_main.py`第10行）
```python
API_URL = "http://localhost:1234/v1/chat/completions"
```
- 默认端口是 `1234`（LM Studio默认值）
- 如使用其他LLM服务器请修改

#### 图形模式（`asl_main.py`第33行）
```python
# 当前（兼容模式）:
p.connect(p.GUI, options="--opengl2")

# 高性能模式（需要好显卡）:
p.connect(p.GUI)
```
- 如果有NVIDIA显卡，可删除 `options="--opengl2"` 获得更好图形
- 如果崩溃请改回原样

---

### 🛠️ 常见问题

| 问题 | 解决方案 |
|------|---------|
| `ModuleNotFoundError: speech_recognition` | 运行: `pip install SpeechRecognition` |
| 语音识别超时 | 1. 检查互联网连接<br>2. 确保麦克风未静音<br>3. 说话声音大一点、慢一点 |
| LLM `Connection Error` | 确认LM Studio服务器运行在1234端口 |
| 机械手动作太慢 | **正常现象** - 闭环控制确保平滑运动 |
| URDF加载错误 | 确认 `my_shadow_hand.urdf` 与脚本在同一目录 |
| PyBullet崩溃 | 在 `p.connect()` 行添加 `options="--opengl2"` |

---

### 📂 项目结构

```
asl_robot_project/
├── asl_main.py              # 主控制脚本（250行）
│   ├── 语音识别模块          # Google Speech API集成
│   ├── LLM接口             # 本地大模型API调用
│   ├── ASL姿态库            # A-Z手势定义
│   ├── 闭环控制            # 关节位置反馈
│   └── PyBullet仿真        # 物理引擎
│
├── my_shadow_hand.urdf      # 机器人模型定义
│   ├── 20个可动关节         # 手指+手腕
│   └── 碰撞网格            # 用于物理模拟
│
├── requirements.txt         # 依赖项
└── README.md               # 文档
```

---

### 🎨 技术亮点

1. **智能纠错算法**
   - 使用LLM根据上下文修复ASR错误
   - 处理同音字: "怎么周" → "怎么走"

2. **闭环运动控制**
   ```python
   # 等待关节到达目标位置±0.15弧度
   while time.time() - start < 2.0:
       curr = p.getJointState(robot_id, joint_id)[0]
       if abs(curr - target) < 0.15:
           break
   ```

3. **ASL手势库**
   - 26个字母 + REST复位姿态
   - 手指缩写: FF(食指), MF(中指), RF(无名指), LF(小指), TH(拇指)
   - 示例A: 所有手指弯曲，拇指稍外展

4. **噪音消除**
   ```python
   r.adjust_for_ambient_noise(source, duration=0.8)
   r.pause_threshold = 1.5  # 防止语音被截断
   ```

---

### 📊 系统性能

| 指标 | 数值 |
|-----|------|
| ASR延迟 | ~2-3秒（Google API） |
| LLM推理 | ~1-2秒（Qwen2.5-1.5B CPU） |
| 手势执行 | ~1-2秒/字母 |
| 关节精度 | ±0.15弧度 |
| 物理时间步 | 240 Hz（PyBullet） |

---

### 🔮 未来改进

- [ ] 添加动态ASL手势（不仅是字母拼写）
- [ ] 支持离线ASR（Whisper集成）
- [ ] 双手协调用于复杂短语
- [ ] 真实机器人部署（UR5 + Leap Hand）
- [ ] Web界面远程控制

---

### 📄 许可证

MIT License - 欢迎用于教育/研究目的

---


