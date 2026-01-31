import pybullet as p
import pybullet_data
import time
import requests
import json
import speech_recognition as sr

# ================= 配置区域 =================
API_URL = "http://localhost:1234/v1/chat/completions"

# 核心提示词：负责纠错、翻译和拆字
SYSTEM_PROMPT = """
You are the intelligent brain of a robotic hand.
Your input comes from Voice Recognition (ASR), which often contains typos or homophone errors.

Task:
1. **CORRECT**: Fix any typos/homophones based on context (e.g., "怎么周" -> "怎么走").
2. **TRANSLATE**: Translate the CORRECTED Chinese to English.
3. **CONVERT**: Convert to uppercase letters sequence.
4. **FORMAT**: Output STRICT JSON.

Example:
Input: "你好怎么周"
Output: {
    "corrected": "你好怎么走", 
    "english": "HELLO HOW TO GO", 
    "sequence": ["H","E","L","L","O"," ","H","O","W"," ","..."]
}
"""

# ================= 仿真初始化 =================
print("正在启动 PyBullet...")
try:
    p.connect(p.GUI, options="--opengl2") # opengl2 保证兼容性
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.resetDebugVisualizerCamera(0.8, 45, -30, [0, 0, 0.5])
    p.loadURDF("plane.urdf")
    robot_id = p.loadURDF("my_shadow_hand.urdf", [0, 0, 0.5], useFixedBase=True)
except Exception as e:
    print(f"❌ 错误: 无法加载 URDF 模型。请确认 'my_shadow_hand.urdf' 在当前目录下。\n详情: {e}")
    exit()

joint_map = {}
for i in range(p.getNumJoints(robot_id)):
    info = p.getJointInfo(robot_id, i)
    if info[2] != p.JOINT_FIXED:
        joint_map[info[1].decode('utf-8')] = i

# ================= ASL 姿态定义 (A-Z) =================
def get_pose_angles(char):
    angles = {name: 0.0 for name in joint_map.keys()}
    def bend(prefix, val=1.6):
        for j in ["J1","J2","J3"]: 
            if f"rh_{prefix}{j}" in angles: angles[f"rh_{prefix}{j}"] = val
    
    char = char.upper()
    if char == "REST": return angles

    if char == "A": 
        for f in ["FF","MF","RF","LF"]: bend(f)
        if "rh_THJ4" in angles: angles["rh_THJ4"] = 0.2
    elif char == "B": 
        if "rh_THJ4" in angles: angles["rh_THJ4"] = 1.2
        if "rh_THJ5" in angles: angles["rh_THJ5"] = 1.0
    elif char == "C": 
        for f in ["FF","MF","RF","LF"]: bend(f, 0.6)
        if "rh_THJ4" in angles: angles["rh_THJ4"] = 0.5
    elif char == "D": 
        for f in ["MF","RF","LF"]: bend(f, 0.8)
        if "rh_THJ3" in angles: angles["rh_THJ3"] = 0.5
    elif char == "E": 
        for f in ["FF","MF","RF","LF"]: bend(f, 1.6)
        if "rh_THJ4" in angles: angles["rh_THJ4"] = 1.2
    elif char == "F": 
        bend("FF", 1.0)
        if "rh_THJ3" in angles: angles["rh_THJ3"] = 0.8
    elif char == "G": 
        for f in ["MF","RF","LF"]: bend(f)
        if "rh_FFJ3" in angles: angles["rh_FFJ3"] = 1.0
    elif char == "H": 
        for f in ["RF","LF"]: bend(f)
    elif char == "I": 
        for f in ["FF","MF","RF"]: bend(f)
        if "rh_THJ4" in angles: angles["rh_THJ4"] = 1.0
    elif char == "J": 
        for f in ["FF","MF","RF"]: bend(f)
        if "rh_THJ4" in angles: angles["rh_THJ4"] = 1.0
        if "rh_WRJ2" in angles: angles["rh_WRJ2"] = 0.3
    elif char == "K": 
        for f in ["RF","LF"]: bend(f)
        if "rh_FFJ3" in angles: angles["rh_FFJ3"] = 0.2
        if "rh_THJ3" in angles: angles["rh_THJ3"] = 0.5
    elif char == "L": 
        for f in ["MF","RF","LF"]: bend(f)
    elif char == "M": 
        for f in ["FF","MF","RF","LF"]: bend(f, 1.4)
        if "rh_THJ4" in angles: angles["rh_THJ4"] = 0.8
    elif char == "N": 
        for f in ["FF","MF","RF","LF"]: bend(f, 1.4)
        if "rh_THJ4" in angles: angles["rh_THJ4"] = 0.8 
    elif char == "O": 
        for f in ["FF","MF","RF","LF"]: bend(f, 1.5)
        if "rh_THJ3" in angles: angles["rh_THJ3"] = 0.6
    elif char == "P": 
        for f in ["RF","LF"]: bend(f)
        bend("MF", 1.0)
    elif char == "Q": 
        for f in ["MF","RF","LF"]: bend(f)
        bend("FF", 1.2)
        if "rh_THJ3" in angles: angles["rh_THJ3"] = 0.8
    elif char == "R": 
        for f in ["RF","LF"]: bend(f)
    elif char == "S": 
        for f in ["FF","MF","RF","LF"]: bend(f)
        if "rh_THJ4" in angles: angles["rh_THJ4"] = 1.0 
        if "rh_THJ2" in angles: angles["rh_THJ2"] = 1.0
    elif char == "T": 
        for f in ["MF","RF","LF"]: bend(f)
        if "rh_FFJ2" in angles: angles["rh_FFJ2"] = 1.2
        if "rh_THJ4" in angles: angles["rh_THJ4"] = 0.8
    elif char == "U": 
        for f in ["RF","LF"]: bend(f)
    elif char == "V": 
        for f in ["RF","LF"]: bend(f)
    elif char == "W": 
        bend("LF")
        if "rh_THJ4" in angles: angles["rh_THJ4"] = 1.2
    elif char == "X": 
        for f in ["MF","RF","LF"]: bend(f)
        def hook(prefix, val=1.6):
            for j in ["J1", "J2"]: angles[f"rh_{prefix}{j}"] = val
        hook("FF", 1.5)
    elif char == "Y": 
        for f in ["FF","MF","RF"]: bend(f)
    elif char == "Z": 
        for f in ["MF","RF","LF"]: bend(f)
    elif char == " ": 
        pass 
    else:
        for f in ["FF","MF","RF","LF"]: bend(f, 0.5)
    return angles

# ================= 闭环运动控制 =================
def execute_sequence(sequence):
    print(f"准备执行序列: {sequence}")
    for char in sequence:
        if char == " ":
            print(">>> (空格)")
            time.sleep(0.5)
            continue
            
        print(f">>> 动作: {char}")
        target_pose = get_pose_angles(char)
        
        # 1. 下达指令
        for j_name, angle in target_pose.items():
            if j_name in joint_map:
                p.setJointMotorControl2(
                    robot_id, joint_map[j_name], 
                    p.POSITION_CONTROL, targetPosition=angle,
                    force=20.0, maxVelocity=2.0
                )
        
        # 2. 闭环检测 (Smart Wait)
        start = time.time()
        while time.time() - start < 2.0: # 2秒超时防止卡死
            p.stepSimulation()
            time.sleep(1./240.)
            all_done = True
            for j_name, target in target_pose.items():
                if j_name in joint_map:
                    curr = p.getJointState(robot_id, joint_map[j_name])[0]
                    if abs(curr - target) > 0.15: # 允许误差范围
                        all_done = False; break
            if all_done: break
        time.sleep(0.1)

# ================= 语音识别 (带容错优化) =================
def get_voice_input():
    r = sr.Recognizer()
    r.pause_threshold = 1.5       # 允许1.5秒停顿，防止把"怎么...走"截断
    r.non_speaking_duration = 1.5 # 防止尾音被吞

    print("\n🎤 正在调整环境噪音... (请静音1秒)")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.8)
        print("🔴 请说话! (Listening...)")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
            print("🔄 识别中...")
            text = r.recognize_google(audio, language='zh-CN')
            text = text.replace("，", " ").replace("。", "") # 清洗标点
            print(f"👂 听到: 【 {text} 】")
            return text
        except Exception as e:
            print(f"❌ 语音未识别: {e}")
            return None

# ================= LLM 调用 =================
def call_llm(text):
    print(f"🧠 发送给大脑纠错: {text} ...")
    try:
        res = requests.post(API_URL, json={
            "model": "local-model",
            "messages": [{"role":"system","content":SYSTEM_PROMPT}, {"role":"user","content":text}],
            "temperature": 0.1, "max_tokens": 500
        }, timeout=None)
        
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            clean = content.replace("```json","").replace("```","").strip()
            s = clean.find('{'); e = clean.rfind('}')
            if s!=-1 and e!=-1:
                return json.loads(clean[s:e+1])
    except Exception as e:
        print(f"❌ 连接错误: {e}")
    return None

# ================= 主程序 =================
print("\n=== Shadow Hand 智能控制系统 ===")
print("操作指南: 按 'v' 键说话，按 'q' 退出")

try:
    while True:
        p.stepSimulation()
        cmd = input("\n输入指令 (v=语音, q=退出): ").strip().lower()
        
        if cmd == 'q': break
        
        text = ""
        if cmd == 'v':
            text = get_voice_input()
        else:
            text = cmd # 支持直接打字

        if text:
            data = call_llm(text)
            if data and "sequence" in data:
                if "corrected" in data:
                    print(f"✨ 智能纠错: {data['corrected']}")
                print(f"📖 翻译结果: {data.get('english', 'Unknown')}")
                execute_sequence(data['sequence'])
                print("🔄 复位...")
                execute_sequence(["REST"])
            else:
                print("❌ LLM 未能解析动作")

except KeyboardInterrupt: pass
finally: p.disconnect()
