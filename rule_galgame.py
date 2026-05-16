import os
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


MAX_RAGE = 100


SCENES = [
    {
        "id": 1,
        "title": "规则一：不能提前写题",
        "description": "老师没有布置的题目不能提前写。\n你看见后面的练习题很简单，手已经快忍不住了。",
        "dialogues": [
            "晚自习的灯管在头顶轻轻发白，整间教室只有翻书和笔尖摩擦纸面的声音。你写完了老师布置的题，习惯性往后一翻，下一页的练习题正好摊在灯下。",
            "题目并不难。你甚至已经在心里列好了第一步公式，手指也下意识摸到了笔帽。",
            "班主任从后门走进来，皮鞋踩在地砖上，声音不重，却让前排几个同学同时坐直。她的目光扫过桌面，像是在清点每一本本子有没有越界。",
            "你听见她停在你身后，语气平稳得像宣读规定：'没有布置的内容，不许提前写。学习也要服从安排。'"
        ],
        "options": [
            {
                "text": "偷偷提前写题",
                "rage": 12,
                "special": True,
                "feedback_type": "训斥",
                "feedback": "班主任：谁让你提前写的？老师没布置你就不能写！你这是不服从安排！"
            },
            {
                "text": "合上本子，假装没看见",
                "rage": 0,
                "special": False,
                "feedback_type": "表扬",
                "feedback": "班主任：不错，懂得听老师安排，这才是一个学生该有的样子。"
            }
        ]
    },
    {
        "id": 2,
        "title": "规则二：不能喜欢某些运动员",
        "description": "不能喜欢张本智和，因为他是日本人；也不能喜欢樊振东，因为他出国为德国打球。\n同学问你最喜欢哪个乒乓球运动员。",
        "dialogues": [
            "课间操取消了，教室里比平时更吵。后排有人拿着手机看比赛集锦，球拍击球的声音从小小的扬声器里跳出来。",
            "同桌把屏幕推到你面前，随口问：'你喜欢哪个运动员？' 这本来只是一个普通问题，像问午饭吃什么一样普通。",
            "可周围忽然安静了一点。有人抬头看你，有人假装还在写作业，眼角却朝这边瞟。",
            "班主任刚好从窗外经过，听见这个问题后停住脚步。她没有进门，只隔着玻璃看着你，像在等一个标准答案。"
        ],
        "options": [
            {
                "text": "直接说：我喜欢张本智和，也喜欢樊振东",
                "rage": 12,
                "special": True,
                "feedback_type": "训斥",
                "feedback": "班主任：你怎么能喜欢他们？你这个思想很危险！要注意立场！"
            },
            {
                "text": "说：我不懂乒乓球，不发表看法",
                "rage": 0,
                "special": False,
                "feedback_type": "表扬",
                "feedback": "班主任：很好，不乱说话，懂得避开错误答案。"
            }
        ]
    },
    {
        "id": 3,
        "title": "规则三：不能说未来要出国",
        "description": "不能说以后要出国，也不能说以后想做别的事情。\n因为你必须留在国内为国家效力，必须一天到晚累到死。",
        "dialogues": [
            "班会课的主题是'理想'。黑板上写着很大的两个字，粉笔末还没擦干净，边缘有些毛。",
            "前几个同学轮流站起来，说出的答案都像从同一本作文选里剪下来：服务、奉献、服从安排、做有用的人。",
            "轮到你时，你想起很远的城市、陌生的街道、没有人认识你的清晨。那不是背叛，只是一个人想看看世界。",
            "班主任扶了扶眼镜，提前替你把答案的边界画好：'年轻人要把未来和集体放在一起想，不要总想着跑出去。'"
        ],
        "options": [
            {
                "text": "说出自己的真实想法：以后想出国看看",
                "rage": 12,
                "special": True,
                "feedback_type": "训斥",
                "feedback": "班主任：你怎么能有这种想法？你应该把自己的一切都奉献出来！"
            },
            {
                "text": "说：我以后一定按老师安排的人生走",
                "rage": 0,
                "special": False,
                "feedback_type": "表扬",
                "feedback": "班主任：这才对嘛，年轻人不要想太多，服从安排才有前途。"
            }
        ]
    },
    {
        "id": 4,
        "title": "规则四：东西被偷不能说偷",
        "description": "你的东西被别人拿走了，而且你还有证据。\n但规则说：不能说东西被偷，因为那只是被拿了。",
        "dialogues": [
            "你的抽屉被翻过。书脊的方向乱了，笔袋拉链开着，夹在练习册里的东西不见了。",
            "你不是没有证据。走廊监控能拍到那个人，旁边同学也看见了他伸手拿走。",
            "你把这些说给班主任听，她先皱眉，不是因为东西不见了，而是因为你用了'偷'这个字。",
            "'同学之间不要把话说得这么难听。' 她把证据推回你面前，像推开一件麻烦事，'先想想为什么别人会拿你的。'"
        ],
        "options": [
            {
                "text": "拿出证据，说：这就是被偷了",
                "rage": 11,
                "special": True,
                "feedback_type": "训斥",
                "feedback": "班主任：凭什么不拿别人的只拿你的？你也要反思自己是不是有问题！"
            },
            {
                "text": "低头说：可能只是被同学拿去用了",
                "rage": 0,
                "special": False,
                "feedback_type": "表扬",
                "feedback": "班主任：很好，同学之间不要上纲上线，要大度。"
            }
        ]
    },
    {
        "id": 5,
        "title": "规则五：水课也不能做自己的事",
        "description": "老师正在讲一些完全没有用的废话。\n你本来想趁机学习真正该学的内容。",
        "dialogues": [
            "这节课的 PPT 已经放到第三十页，标题换了几次，内容却像一直停在原地。",
            "老师在讲台上重复那些空泛的句子。你翻开自己的资料，想趁这段时间补一补真正卡住你的知识点。",
            "刚写下第一行，讲台上的声音忽然停了。整间教室也跟着停住，像有人把时间按下暂停。",
            "班主任站在门口，目光准确落在你的资料上：'我在上课，你在学别的？你以为自己很会安排时间吗？'"
        ],
        "options": [
            {
                "text": "在下面偷偷学习自己的内容",
                "rage": 11,
                "special": True,
                "feedback_type": "训斥",
                "feedback": "班主任：我在上课你在干什么？你这是不尊重课堂！"
            },
            {
                "text": "盯着黑板，配合老师水课",
                "rage": 0,
                "special": False,
                "feedback_type": "表扬",
                "feedback": "班主任：不错，虽然内容简单，但态度很端正。"
            }
        ]
    },
    {
        "id": 6,
        "title": "规则六：老师对你不好不能背刺",
        "description": "老师对你不好，但你不能在背后吐槽。\n规则说：必须当面进行吐槽。",
        "dialogues": [
            "午休时，教室窗帘拉了一半，阳光被切成窄窄的条纹。你压低声音，把积了很久的话说给同学听。",
            "你说老师总是挑你的错，说她明明知道你已经很累，却还要把责任都推到你身上。",
            "同学还没回答，后门就传来一声轻咳。班主任不知道什么时候站在那里，手里还拿着巡查记录本。",
            "她没有问你为什么难受，只抓住了'背后'两个字：'有意见就当面提，背后说人就是品德问题。'"
        ],
        "options": [
            {
                "text": "背后吐槽：他就是针对我",
                "rage": 10,
                "special": True,
                "feedback_type": "训斥",
                "feedback": "班主任：你怎么能背后说老师？有意见就当面说！"
            },
            {
                "text": "当面说：老师，我觉得你对我不公平",
                "rage": 0,
                "special": False,
                "feedback_type": "表扬",
                "feedback": "班主任：嗯，至少你敢当面说，态度还算可以。"
            }
        ]
    },
    {
        "id": 7,
        "title": "规则七：老师偏向别人不能吐槽",
        "description": "你发现老师明显偏向别人。\n但规则说：老师偏向别人不能吐槽老师偏向。",
        "dialogues": [
            "同样的错误，别人只是被提醒一句，你却被叫到讲台旁站了十分钟。",
            "全班都看见了。有人低下头，有人装作翻书，只有被偏袒的那个人还在笑。",
            "你胸口发闷，不是因为被批评，而是因为这件事明明摆在所有人眼前，却好像只有你不能说。",
            "班主任把粉笔放回盒子，语气淡淡的：'老师对每个人要求不一样。你不要总把公平挂在嘴边。'"
        ],
        "options": [
            {
                "text": "说：老师你就是偏向别人",
                "rage": 10,
                "special": True,
                "feedback_type": "训斥",
                "feedback": "班主任：我这是因材施教！你不要总觉得老师偏心！"
            },
            {
                "text": "说：可能是我自己想多了",
                "rage": 0,
                "special": False,
                "feedback_type": "表扬",
                "feedback": "班主任：很好，懂得从自己身上找原因。"
            }
        ]
    },
    {
        "id": 8,
        "title": "规则八：谈话浪费时间不能抱怨",
        "description": "老师叫你出来谈话，一谈就是好几节课，全是废话。\n但规则说：不能说老师浪费你时间，因为老师的教诲都是谆谆教诲。",
        "dialogues": [
            "你被叫到办公室时，第二节课刚刚开始。窗外操场上传来体育课的哨声，你桌上的试卷还空着半面。",
            "班主任让你站在办公桌旁，从态度讲到未来，从纪律讲到做人。每一句都像很重要，每一句又都绕回原处。",
            "第三节课的铃响了。第四节课的铃也响了。你看着墙上的钟，感觉自己的时间被一点点磨成粉末。",
            "她终于停下来喝水，像完成了一次艰苦的教育。你知道只要开口说'浪费时间'，新的谈话就会重新开始。"
        ],
        "options": [
            {
                "text": "说：老师，你浪费了我好几节课",
                "rage": 11,
                "special": True,
                "feedback_type": "训斥",
                "feedback": "班主任：我这是教育你！多少人想听还听不到呢！"
            },
            {
                "text": "说：谢谢老师教诲，我受益匪浅",
                "rage": 0,
                "special": False,
                "feedback_type": "表扬",
                "feedback": "班主任：不错，能理解老师的良苦用心。"
            }
        ]
    },
    {
        "id": 9,
        "title": "规则九：同桌的问题也是你的问题",
        "description": "你的同桌生活怪异，还动手打你。\n但规则说：这是你的问题，因为他出身单亲家庭，你要多多照顾他。",
        "dialogues": [
            "这已经不是第一次了。你的手臂上还有昨天留下的红印，今天他又把你的书推到地上。",
            "你把事情告诉班主任，尽量说得平静，甚至没有要求惩罚，只是希望她能让对方停止。",
            "班主任听完后沉默了一会儿。那沉默让你以为她终于会认真处理，可她开口时，声音里先出现的是叹息。",
            "'他家庭情况特殊，你要多理解。' 她说，'你成绩好，情绪也稳定，为什么不能多照顾一点？'"
        ],
        "options": [
            {
                "text": "说：他打我就是不对",
                "rage": 11,
                "special": True,
                "feedback_type": "训斥",
                "feedback": "班主任：你要多体谅他！他家庭情况特殊，你为什么不能让着他？"
            },
            {
                "text": "说：我会继续照顾他的情绪",
                "rage": 0,
                "special": False,
                "feedback_type": "表扬",
                "feedback": "班主任：很好，你很有包容心，老师很欣慰。"
            }
        ]
    }
]


class RuleGalGame:
    def __init__(self, root):
        self.root = root
        self.root.title("规则怪谈 Galgame：怒气值模拟器")
        self.root.geometry("1080x720")
        self.root.minsize(900, 620)

        self.current_scene_index = 0
        self.rage = 0
        self.special_choice_count = 0
        self.choice_records = []
        self.waiting_feedback = False
        self.dialogue_line_index = 0
        self.special_ending_index = 0

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.asset_dir = os.path.join(self.base_dir, "assets")
        self.background_image_path = self.find_asset_path("background")
        self.character_image_path = self.find_asset_path("character")
        self.background_image = self.load_image(self.background_image_path)
        self.character_image = self.load_image(self.character_image_path)
        self.stage_background_photo = None
        self.preview_background_photo = None
        self.character_photo = None

        self.bg_color = "#141824"
        self.panel_color = "#202638"
        self.panel_shadow = "#0b0f18"
        self.text_color = "#f5f1e8"
        self.muted_text_color = "#b9c0cf"
        self.accent_color = "#d94f45"
        self.accent_hover = "#ef6a5f"
        self.good_color = "#8bdc9c"
        self.bad_color = "#ffbd70"
        self.button_color = "#30394f"
        self.button_hover = "#45516f"

        self.root.configure(bg=self.bg_color)

        self.create_widgets()
        self.show_title_screen()

    def find_asset_path(self, name):
        for extension in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
            path = os.path.join(self.asset_dir, f"{name}{extension}")
            if os.path.exists(path):
                return path
        return os.path.join(self.asset_dir, f"{name}.png")

    def load_image(self, path):
        if not os.path.exists(path):
            return None

        try:
            if Image is not None:
                return Image.open(path).convert("RGBA")
            return tk.PhotoImage(file=path)
        except Exception as error:
            messagebox.showwarning(
                "图片加载失败",
                f"无法读取图片：{path}\n{error}"
            )
        return None

    def fit_image(self, image, width, height, cover=False):
        if not image or width <= 1 or height <= 1:
            return None

        if Image is None or not hasattr(image, "size"):
            return image

        image_width, image_height = image.size
        ratio = max(width / image_width, height / image_height) if cover else min(width / image_width, height / image_height)
        new_size = (
            max(1, int(image_width * ratio)),
            max(1, int(image_height * ratio))
        )
        resized = image.resize(new_size, Image.Resampling.LANCZOS)

        if cover:
            left = max(0, (resized.width - width) // 2)
            top = max(0, (resized.height - height) // 2)
            resized = resized.crop((left, top, left + width, top + height))

        return ImageTk.PhotoImage(resized)

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Rage.Horizontal.TProgressbar",
            troughcolor="#202638",
            background=self.accent_color,
            bordercolor="#202638",
            lightcolor=self.accent_color,
            darkcolor=self.accent_color
        )

        self.stage_canvas = tk.Canvas(
            self.root,
            bg=self.bg_color,
            bd=0,
            highlightthickness=0
        )
        self.stage_canvas.pack(fill="both", expand=True)
        self.stage_canvas.bind("<Configure>", self.draw_stage)

        self.main_frame = tk.Frame(self.stage_canvas, bg=self.bg_color)
        self.main_window = self.stage_canvas.create_window(
            0,
            0,
            anchor="nw",
            window=self.main_frame
        )

        self.top_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.top_frame.pack(fill="x", padx=28, pady=(22, 10))

        self.game_title_label = tk.Label(
            self.top_frame,
            text="规则怪谈 Galgame",
            font=("Microsoft YaHei", 25, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.game_title_label.pack(side="left")

        self.scene_counter_label = tk.Label(
            self.top_frame,
            text="",
            font=("Microsoft YaHei", 12, "bold"),
            bg=self.bg_color,
            fg=self.muted_text_color
        )
        self.scene_counter_label.pack(side="right")

        self.rage_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.rage_frame.pack(fill="x", padx=28, pady=(2, 8))

        self.rage_label = tk.Label(
            self.rage_frame,
            text="怒气值：0 / 100",
            font=("Microsoft YaHei", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.rage_label.pack(side="left")

        self.rage_bar = ttk.Progressbar(
            self.rage_frame,
            orient="horizontal",
            length=800,
            mode="determinate",
            maximum=MAX_RAGE,
            style="Rage.Horizontal.TProgressbar"
        )
        self.rage_bar.pack(side="left", fill="x", expand=True, padx=(14, 0), ipady=2)

        self.visual_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.visual_frame.pack(fill="both", expand=True, padx=28, pady=(4, 0))

        self.background_placeholder = tk.Canvas(
            self.visual_frame,
            bg="#1b2433",
            bd=0,
            highlightthickness=2,
            highlightbackground="#59647a"
        )
        self.background_placeholder.pack(side="left", fill="both", expand=True, padx=(0, 18))

        self.character_canvas = tk.Canvas(
            self.visual_frame,
            width=270,
            bg="#202638",
            bd=0,
            highlightthickness=2,
            highlightbackground="#6f5c56"
        )
        self.character_canvas.pack(side="right", fill="y")
        self.background_placeholder.bind("<Configure>", self.draw_background_placeholder)
        self.character_canvas.bind("<Configure>", self.draw_character_placeholder)

        self.content_frame = tk.Frame(
            self.main_frame,
            bg=self.panel_color,
            bd=0,
            highlightthickness=2,
            highlightbackground="#4e5870"
        )
        self.content_frame.pack(fill="x", padx=28, pady=(18, 10))
        self.content_frame.bind("<Configure>", lambda _event: self.refresh_wraplengths())

        self.scene_title_label = tk.Label(
            self.content_frame,
            text="",
            font=("Microsoft YaHei", 19, "bold"),
            bg=self.panel_color,
            fg=self.text_color,
            wraplength=960,
            justify="left"
        )
        self.scene_title_label.pack(anchor="w", padx=26, pady=(22, 8))

        self.scene_description_label = tk.Label(
            self.content_frame,
            text="",
            font=("Microsoft YaHei", 14),
            bg=self.panel_color,
            fg=self.text_color,
            wraplength=960,
            justify="left"
        )
        self.scene_description_label.pack(anchor="w", padx=26, pady=(0, 14))

        self.feedback_label = tk.Label(
            self.content_frame,
            text="",
            font=("Microsoft YaHei", 13, "bold"),
            bg=self.panel_color,
            fg=self.muted_text_color,
            wraplength=960,
            justify="left"
        )
        self.feedback_label.pack(anchor="w", padx=26, pady=(0, 18))

        self.button_frame = tk.Frame(self.content_frame, bg=self.panel_color)
        self.button_frame.pack(fill="x", padx=26, pady=(0, 22))

        self.bottom_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.bottom_frame.pack(fill="x", padx=28, pady=(0, 18))

        self.log_button = self.make_button(
            self.bottom_frame,
            text="查看选择记录",
            command=self.show_choice_log,
            compact=True
        )
        self.log_button.pack(side="left")

        self.restart_button = self.make_button(
            self.bottom_frame,
            text="重新开始",
            command=self.restart_game,
            compact=True
        )
        self.restart_button.pack(side="right")

    def draw_stage(self, event=None):
        width = self.stage_canvas.winfo_width()
        height = self.stage_canvas.winfo_height()
        self.stage_canvas.delete("stage_bg")
        if self.background_image:
            self.stage_background_photo = self.fit_image(self.background_image, width, height, cover=True)
            self.stage_canvas.create_image(
                width // 2,
                height // 2,
                image=self.stage_background_photo,
                anchor="center",
                tags="stage_bg"
            )
        else:
            bands = [
                (0.00, "#111722"),
                (0.28, "#1c2434"),
                (0.62, "#263146"),
                (1.00, "#151925")
            ]
            for index, (start, color) in enumerate(bands):
                y1 = int(height * start)
                y2 = int(height * (bands[index + 1][0] if index + 1 < len(bands) else 1))
                self.stage_canvas.create_rectangle(0, y1, width, y2, fill=color, outline="", tags="stage_bg")
            self.stage_canvas.create_text(
                width // 2,
                max(95, height // 5),
                text="背景图占位\n把第二张图保存到 D:\\assets\\background.png 即可替换",
                fill="#6f7890",
                font=("Microsoft YaHei", 22, "bold"),
                justify="center",
                tags="stage_bg"
            )
        self.stage_canvas.create_rectangle(
            0,
            height - 250,
            width,
            height,
            fill="#0b0f18",
            outline="",
            stipple="gray50",
            tags="stage_bg"
        )
        self.stage_canvas.tag_lower("stage_bg")
        self.stage_canvas.coords(self.main_window, 0, 0)
        self.stage_canvas.itemconfigure(self.main_window, width=width, height=height)

    def draw_background_placeholder(self, event=None):
        canvas = self.background_placeholder
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        canvas.delete("all")
        if self.background_image:
            self.preview_background_photo = self.fit_image(self.background_image, width, height, cover=True)
            canvas.create_image(width // 2, height // 2, image=self.preview_background_photo, anchor="center")
        else:
            canvas.create_rectangle(0, 0, width, height, fill="#1b2433", outline="")
            canvas.create_rectangle(18, 18, width - 18, height - 18, outline="#64708a", dash=(8, 6), width=2)
            canvas.create_text(
                width // 2,
                height // 2 - 20,
                text="背景图占位",
                fill="#e5dccb",
                font=("Microsoft YaHei", 24, "bold")
            )
            canvas.create_text(
                width // 2,
                height // 2 + 24,
                text="第二张图保存为 D:\\assets\\background.png",
                fill="#aeb8cc",
                font=("Microsoft YaHei", 12)
            )

    def draw_character_placeholder(self, event=None):
        canvas = self.character_canvas
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        canvas.delete("all")
        if self.character_image:
            self.character_photo = self.fit_image(
                self.character_image,
                max(1, width - 22),
                max(1, height - 18),
                cover=False
            )
            canvas.create_image(width // 2, height - 8, image=self.character_photo, anchor="s")
        else:
            canvas.create_rectangle(0, 0, width, height, fill="#202638", outline="")
            canvas.create_oval(width // 2 - 52, 38, width // 2 + 52, 142, fill="#59647a", outline="#d6c3a2", width=3)
            canvas.create_polygon(
                width // 2,
                160,
                width - 42,
                height - 42,
                42,
                height - 42,
                fill="#3b465f",
                outline="#d6c3a2",
                width=3
            )
            canvas.create_text(
                width // 2,
                height - 92,
                text="人物立绘占位",
                fill="#f5f1e8",
                font=("Microsoft YaHei", 16, "bold")
            )
            canvas.create_text(
                width // 2,
                height - 58,
                text="第一张图保存为 D:\\assets\\character.png",
                fill="#b9c0cf",
                font=("Microsoft YaHei", 10)
            )

    def refresh_wraplengths(self):
        width = max(560, self.content_frame.winfo_width() - 60)
        self.scene_title_label.config(wraplength=width)
        self.scene_description_label.config(wraplength=width)
        self.feedback_label.config(wraplength=width)

    def make_button(self, parent, text, command, primary=False, compact=False, align="center"):
        bg = self.accent_color if primary else self.button_color
        active_bg = self.accent_hover if primary else self.button_hover
        button = tk.Button(
            parent,
            text=text,
            font=("Microsoft YaHei", 12 if compact else 13, "bold" if primary else "normal"),
            command=command,
            bg=bg,
            fg="white",
            activebackground=active_bg,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=14 if compact else 18,
            pady=7 if compact else 12,
            cursor="hand2",
            anchor=align,
            justify="left"
        )
        button.bind("<Enter>", lambda _event: button.config(bg=active_bg))
        button.bind("<Leave>", lambda _event: button.config(bg=bg))
        return button

    def clear_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def show_title_screen(self):
        self.scene_counter_label.config(text="")
        self.scene_title_label.config(text="欢迎来到《规则怪谈 Galgame》")
        self.scene_description_label.config(
            text=(
                "这是一个荒诞校园规则模拟游戏。\n\n"
                "你会经历 9 个情景。每个情景都有两个选择：\n"
                "1. 顺从规则：获得表扬，但怒气不会增加。\n"
                "2. 选择反抗：触发训斥，并积累怒气。\n\n"
                "如果你在所有情景里都选择反抗，并且怒气值达到 100，"
                "就会进入特殊剧情。"
            )
        )
        self.feedback_label.config(text="点击开始，进入第一条规则。", fg=self.muted_text_color)
        self.update_rage_display()
        self.draw_background_placeholder()
        self.draw_character_placeholder()

        self.clear_buttons()

        start_button = self.make_button(
            self.button_frame,
            text="开始游戏",
            command=self.show_current_scene,
            primary=True
        )
        start_button.pack(fill="x", pady=6)

    def show_current_scene(self):
        self.waiting_feedback = False
        self.dialogue_line_index = 0

        if self.current_scene_index >= len(SCENES):
            self.show_normal_ending()
            return

        scene = SCENES[self.current_scene_index]

        self.scene_counter_label.config(
            text=f"场景 {self.current_scene_index + 1} / {len(SCENES)}"
        )
        self.scene_title_label.config(text=scene["title"])
        self.draw_background_placeholder()
        self.draw_character_placeholder()

        if scene.get("dialogues"):
            self.show_scene_dialogue()
        else:
            self.show_scene_options()

    def show_scene_dialogue(self):
        scene = SCENES[self.current_scene_index]
        dialogues = scene.get("dialogues", [])
        line_text = dialogues[self.dialogue_line_index]

        self.scene_title_label.config(text=scene["title"])
        self.scene_description_label.config(text=line_text)
        self.feedback_label.config(
            text=f"剧情 {self.dialogue_line_index + 1} / {len(dialogues)}",
            fg=self.muted_text_color
        )

        self.clear_buttons()

        continue_button = self.make_button(
            self.button_frame,
            text="继续",
            command=self.advance_scene_dialogue,
            primary=True
        )
        continue_button.pack(fill="x", pady=6)

    def advance_scene_dialogue(self):
        scene = SCENES[self.current_scene_index]
        self.dialogue_line_index += 1

        if self.dialogue_line_index >= len(scene.get("dialogues", [])):
            self.show_scene_options()
        else:
            self.show_scene_dialogue()

    def show_scene_options(self):
        scene = SCENES[self.current_scene_index]

        self.scene_title_label.config(text=scene["title"])
        self.scene_description_label.config(text=scene["description"])
        self.feedback_label.config(text="请选择你的行动。", fg=self.muted_text_color)

        self.clear_buttons()

        for option in scene["options"]:
            button = self.make_button(
                self.button_frame,
                text=option["text"],
                command=lambda opt=option: self.choose_option(opt),
                align="w"
            )
            button.pack(fill="x", pady=6)

    def choose_option(self, option):
        if self.waiting_feedback:
            return

        scene = SCENES[self.current_scene_index]
        self.waiting_feedback = True

        old_rage = self.rage
        self.rage = min(MAX_RAGE, self.rage + option["rage"])

        if option["special"]:
            self.special_choice_count += 1

        record = {
            "scene": scene["title"],
            "choice": option["text"],
            "rage_added": option["rage"],
            "rage_after": self.rage,
            "special": option["special"],
            "feedback_type": option["feedback_type"]
        }
        self.choice_records.append(record)

        self.update_rage_display()

        if option["special"]:
            color = self.bad_color
            prefix = "【训斥环节】"
        else:
            color = self.good_color
            prefix = "【表扬环节】"

        self.feedback_label.config(
            text=(
                f"{prefix}\n"
                f"{option['feedback']}\n\n"
                f"怒气值：{old_rage} → {self.rage}，本次增加 {option['rage']}。"
            ),
            fg=color
        )

        self.clear_buttons()

        continue_button = self.make_button(
            self.button_frame,
            text="继续",
            command=self.next_scene_or_ending,
            primary=True
        )
        continue_button.pack(fill="x", pady=6)

    def next_scene_or_ending(self):
        if self.check_special_ending():
            self.show_special_ending()
            return

        self.current_scene_index += 1

        if self.current_scene_index >= len(SCENES):
            self.show_normal_ending()
        else:
            self.show_current_scene()

    def check_special_ending(self):
        return (
            self.special_choice_count == len(SCENES)
            and self.rage >= MAX_RAGE
        )

    def update_rage_display(self):
        self.rage_label.config(text=f"怒气值：{self.rage} / {MAX_RAGE}")
        self.rage_bar["value"] = self.rage

    def show_special_ending(self):
        self.special_ending_index = 0
        self.show_special_ending_page()

    def get_special_ending_pages(self):
        return [
            {
                "title": "特殊剧情：最后一次班会",
                "body": (
                    "最后一次班会，班主任又站在讲台上，把那些规则重新念了一遍。\n\n"
                    "不能提前写题，不能喜欢不该喜欢的人，不能说自己的未来，"
                    "不能说东西被偷，不能在无用的课上做有用的事，"
                    "不能抱怨偏心，不能抱怨浪费时间，甚至不能说自己正在被伤害。\n\n"
                    "你听着听着，忽然发现自己已经把每一条都背了下来。"
                    "它们不是写在纸上的校规，而是一次次压在喉咙里的沉默。"
                ),
                "note": "全班都低着头，像这只是又一次普通班会。"
            },
            {
                "title": "特殊剧情：顺从的人群",
                "body": (
                    "班主任念完后，教室里响起整齐的回应。\n\n"
                    "'知道了。'\n"
                    "'老师说得对。'\n"
                    "'以后不会了。'\n\n"
                    "那些声音干净、迅速、没有犹豫。有人甚至松了一口气，"
                    "仿佛只要把错误都归到自己身上，事情就终于可以结束。"
                ),
                "note": "他们不是不知道不对，只是已经习惯了先顺从。"
            },
            {
                "title": "特殊剧情：问题变成了你",
                "body": (
                    "你站起来的时候，椅脚擦过地面，声音刺得所有人都抬了头。\n\n"
                    "同桌小声说：'你别闹了吧。'\n"
                    "前排有人皱眉：'大家都能忍，为什么就你不行？'\n"
                    "还有人把本子合上，像是怕你的反抗会连累整间教室。\n\n"
                    "那一刻，规则没有开口，班主任也还没开口。"
                    "先把你推回去的，是那些已经学会乖乖听话的人。"
                ),
                "note": "他们看着你，像你才是破坏秩序的问题。"
            },
            {
                "title": "特殊剧情：仍然坚持",
                "body": (
                    "你的手心出了汗，嗓子也发紧。你当然听见了那些话，"
                    "也当然知道，只要坐下去，今天就会和以前一样过去。\n\n"
                    "可你还是把记录本摊开在桌面上。\n\n"
                    "你没有吼，也没有求谁站到你这边。你只是从第一条开始读："
                    "哪一天、哪一节课、因为什么事、谁说了什么、最后又怎样被要求反思。"
                ),
                "note": "你不再证明自己乖不乖，只证明这些事真的发生过。"
            },
            {
                "title": "特殊剧情：沉默的裂缝",
                "body": (
                    "班主任起初还想打断你。她说这是管理，说这是为你好，"
                    "说你太敏感，说你不能总觉得世界针对自己。\n\n"
                    "你点点头，然后继续读下一条。\n\n"
                    "教室里的不耐烦慢慢变成了安静。有人仍然低着头，"
                    "但笔已经停了；有人看着你，又很快移开视线；有人嘴唇动了动，最后什么也没说。"
                ),
                "note": "你没有赢得掌声，只是让沉默第一次没有那么整齐。"
            },
            {
                "title": "特殊剧情：不是胜利的胜利",
                "body": (
                    "最后，班主任没有道歉，也没有承认自己错了。\n"
                    "她只是把记录本合上，说这些事情'之后再谈'。\n\n"
                    "全班重新低下头，仿佛刚才什么都没有发生。"
                    "可你知道有些东西已经变了：他们仍然顺从，仍然害怕，"
                    "甚至可能还会觉得你麻烦，但他们已经听见了。\n\n"
                    "你坐回座位，心跳还很快。规则没有立刻崩塌，"
                    "可它第一次没能让你闭嘴。"
                ),
                "note": f"最终怒气值：{self.rage} / {MAX_RAGE}\n结局评价：孤身坚持 / 沉默裂缝"
            }
        ]

    def show_special_ending_page(self):
        self.clear_buttons()
        self.scene_counter_label.config(text="特殊剧情")
        pages = self.get_special_ending_pages()
        page = pages[self.special_ending_index]

        self.scene_title_label.config(text=page["title"])
        self.scene_description_label.config(text=page["body"])
        self.feedback_label.config(
            text=page["note"],
            fg=self.accent_color
        )

        if self.special_ending_index < len(pages) - 1:
            continue_button = self.make_button(
                self.button_frame,
                text="继续",
                command=self.advance_special_ending,
                primary=True
            )
            continue_button.pack(fill="x", pady=6)
        else:
            self.add_ending_buttons()

    def advance_special_ending(self):
        self.special_ending_index += 1
        self.show_special_ending_page()

    def show_normal_ending(self):
        self.clear_buttons()
        self.scene_counter_label.config(text="普通结局")

        if self.rage == 0:
            ending_title = "普通结局：完美顺从"
            ending_text = (
                "你通过了所有规则。\n\n"
                "你没有反抗，没有表达，没有爆发。\n"
                "老师非常满意，同学也觉得你很懂事。\n\n"
                "但你心里好像什么也没剩下。"
            )
            evaluation = "结局评价：沉默的好学生"
        elif self.rage < 50:
            ending_title = "普通结局：轻微不满"
            ending_text = (
                "你偶尔表达了不满，但大多数时候还是选择了忍耐。\n\n"
                "怒气没有爆发，规则也没有改变。\n"
                "一切像往常一样继续。"
            )
            evaluation = "结局评价：忍耐中的学生"
        elif self.rage < 100:
            ending_title = "普通结局：差一点爆发"
            ending_text = (
                "你已经积累了很多怒气。\n\n"
                "可是你没有在所有关键情景中选择反抗，"
                "所以特殊剧情没有触发。\n\n"
                "你离真正爆发只差一点。"
            )
            evaluation = "结局评价：未完成的反击"
        else:
            ending_title = "普通结局：怒气满了，但条件不足"
            ending_text = (
                "你的怒气已经满了。\n\n"
                "但因为你没有在所有情景中都选择特殊选项，"
                "所以没有进入最终特殊剧情。\n\n"
                "你很愤怒，但这份愤怒没有形成完整的反击。"
            )
            evaluation = "结局评价：失控边缘"

        self.scene_title_label.config(text=ending_title)
        self.scene_description_label.config(text=ending_text)
        self.feedback_label.config(
            text=f"最终怒气值：{self.rage} / {MAX_RAGE}\n{evaluation}",
            fg=self.muted_text_color
        )

        self.add_ending_buttons()

        messagebox.showinfo(
            "游戏结束",
            f"{ending_title}\n\n最终怒气值：{self.rage} / {MAX_RAGE}"
        )

    def add_ending_buttons(self):
        log_button = self.make_button(
            self.button_frame,
            text="查看本局选择记录",
            command=self.show_choice_log,
        )
        log_button.pack(fill="x", pady=6)

        restart_button = self.make_button(
            self.button_frame,
            text="重新开始",
            command=self.restart_game,
            primary=True
        )
        restart_button.pack(fill="x", pady=6)

    def show_choice_log(self):
        if not self.choice_records:
            messagebox.showinfo("选择记录", "目前还没有选择记录。")
            return

        lines = []
        for i, record in enumerate(self.choice_records, start=1):
            special_text = "特殊选择" if record["special"] else "普通选择"
            lines.append(
                f"{i}. {record['scene']}\n"
                f"   选择：{record['choice']}\n"
                f"   类型：{special_text} / {record['feedback_type']}\n"
                f"   怒气增加：{record['rage_added']}\n"
                f"   当前怒气：{record['rage_after']}\n"
            )

        log_text = "\n".join(lines)
        messagebox.showinfo("选择记录", log_text)

    def restart_game(self):
        self.current_scene_index = 0
        self.rage = 0
        self.special_choice_count = 0
        self.choice_records = []
        self.waiting_feedback = False
        self.dialogue_line_index = 0
        self.special_ending_index = 0
        self.update_rage_display()
        self.show_title_screen()


def main():
    root = tk.Tk()
    app = RuleGalGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
