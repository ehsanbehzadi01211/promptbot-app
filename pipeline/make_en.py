"""English YouTube Shorts specs -> scripts_en.json (rendered with build7, lang=en)."""
import json

FOOT = ("\n\nFollow for daily AI tips:\n▶️ YouTube: https://youtube.com/@ehbehzad\n📷 Instagram: https://instagram.com/ehbehzad")

def S(t, bg, voice, **k):
    d = {"type": t, "bg": bg, "voice": voice}; d.update(k); return d

V = {}

V["en01_think"] = dict(
    tag="AI EXPLAINED", accent="#2fb8ff", accent2="#35e0a1", post="392979808", uuid="-4936055",
    title="Does ChatGPT Really Think? Explained in 30 Seconds #shorts",
    desc="Does ChatGPT actually think? Here is how it really writes an answer: it predicts the next word, one word at a time. That is also why it can be confidently wrong.\n\nUse it for ideas and drafts, and always check the facts yourself.",
    tags=["ChatGPT", "how ChatGPT works", "AI explained", "artificial intelligence", "LLM", "AI tips", "shorts"],
    scenes=[
        S("hook", "s512055248", "Does ChatGPT really think? Here's the answer in thirty seconds.", title="Does ChatGPT\nreally [[think?]]", sub="The answer in 30 seconds"),
        S("point", "s573012784", "First, these models are trained on a huge amount of text. Books, websites, articles.", num="1", kicker="Step 1", title="It read a huge\namount of text", sub="During training", chips=["Books", "Websites", "Articles"]),
        S("io", "s624757079", "Then they do one thing: predict the next word. Today the weather is really... hot.", kicker="Its real job", icon="spark", inp="Today the weather is really…", out="hot 62% · cold 21%"),
        S("point", "s602810685", "Word by word, very fast. That's how the whole answer gets built.", num="2", kicker="Step 2", title="Word by word", sub="That's how every answer is built"),
        S("point", "s615849265", "That's why it's sometimes confidently wrong. It looks for the likely answer, not always the true one.", mark="bad", num="!", kicker="The catch", title="That's why it's\nsometimes wrong", sub="Likely answer ≠ correct answer"),
        S("cta", "s539425946", "So use it for ideas and drafts, but check the facts yourself. Subscribe to learn more.", title="Great for drafts.\n[[Check the facts]]", sub="Subscribe for more AI tips"),
    ])

V["en02_claude_ws"] = dict(
    tag="AI NEWS", accent="#d97757", accent2="#ffffff", post="392979866", uuid="84297719",
    title="Claude Now Works Inside Google Docs, Sheets & Slides #shorts",
    desc="Anthropic's Claude now works directly inside Google Docs, Sheets and Slides, no more copy and paste.\n\n• Docs: fix and rewrite your sentences\n• Sheets: formulas, pivot tables and charts\n• Slides: builds slides in your own template\n\nBy default it asks before making edits. It's in beta for paid Claude plans.\n\nWhich one do you use most? Comment Docs, Sheets or Slides 👇",
    tags=["Claude", "Anthropic", "Google Docs", "Google Sheets", "Google Slides", "AI news", "Claude AI", "shorts"],
    scenes=[
        S("hook", "s538935488", "Claude just landed inside Google Docs. And Sheets, and Slides. No more copy and paste.", title="Claude is now in\n[[Google Docs]]", sub="Plus Sheets and Slides"),
        S("steps", "s740481635", "Here's what it does in each one. In Docs, it fixes and rewrites your sentences. In Sheets, formulas, pivot tables and charts. In Slides, it builds slides in your own template.", kicker="What it does in each", items=[["Docs", "Fixes and rewrites your text"], ["Sheets", "Formulas, pivot tables, charts"], ["Slides", "Builds slides in your template"]]),
        S("point", "s774208663", "And relax: by default, it asks before every edit.", mark="good", num="✓", kicker="Good to know", title="It asks before\nevery edit", sub="Default mode: Ask before edits"),
        S("point", "s550108264", "For now, it's in beta, for paid Claude plans.", num="!", kicker="For now", title="Beta, for\npaid plans", sub="Claude Pro starts at $20/month"),
        S("ask", "s573012784", "Which one do you use the most? Tell me in the comments.", title="Which one do you\n[[use the most?]]", chips=["Docs", "Sheets", "Slides"]),
    ])

V["en03_imgprompt"] = dict(
    tag="AI IMAGES", accent="#ff8a3d", accent2="#ffd23f", post="392979898", uuid="34490257",
    title="The 4-Part ChatGPT Image Prompt Formula #shorts",
    desc="Your ChatGPT images look boring? The problem is the prompt.\n\nThe 4-part formula:\n1. Subject: exactly what you want\n2. Style: photo, watercolor, 3D\n3. Light: e.g. golden sunset light\n4. Frame: close-up or wide, vertical or horizontal\n\nExample: \"an orange cat on a window ledge, watercolor style, golden sunset light, close-up\"\n\nDon't like it? Don't start over. Just say: \"same, but at night\".",
    tags=["ChatGPT image", "AI image prompt", "prompt formula", "AI art", "ChatGPT tips", "image generation", "shorts"],
    scenes=[
        S("hook", "s540684977", "Your ChatGPT images look boring? The problem is your prompt.", title="Your AI images\nlook [[boring?]]", sub="It's the prompt"),
        S("steps", "s538935488", "Use this four part formula. Subject: exactly what you want. Style: photo, watercolor, or 3D. Light: like golden sunset light. And frame: close-up or wide, vertical or horizontal.", kicker="The 4-part image formula", items=[["Subject", "Exactly what you want"], ["Style", "Photo, watercolor, 3D"], ["Light", "e.g. golden sunset"], ["Frame", "Close or wide, vertical or not"]]),
        S("compare", "s799936566", "Instead of: draw a cat. Write: an orange cat on a window ledge, watercolor style, sunset light, close-up.", kicker="Example", title="See the difference", bad="Draw a cat", good="An orange cat on a window ledge, watercolor, golden sunset light, close-up"),
        S("point", "s524369452", "Don't like it? Don't start over. Just say: same, but at night.", mark="good", num="★", kicker="Pro tip", title="Change just\none part", sub="Say: \"same, but at night\""),
        S("cta", "s577793282", "Save this, and try it today.", title="Save it and\n[[try it today]]", sub="Subscribe for the next part"),
    ])

V["en04_edit"] = dict(
    tag="AI PHOTO EDIT", accent="#ff8a3d", accent2="#5fd3ff", post="392979926", uuid="21621931",
    title="Edit Photos Inside ChatGPT, No Photoshop Needed #shorts",
    desc="You can edit images right inside ChatGPT, no Photoshop.\n\nTap an image to open the editing tools, or upload your own photo and say what to change.\n\n4 useful tools:\n• Remove background in one click\n• Eraser for unwanted objects\n• Resize, e.g. for stories\n• Comment: write on the image what should change\n\nOnly edit photos of other people with their permission.",
    tags=["ChatGPT", "photo editing", "AI photo editor", "remove background", "ChatGPT images", "AI tools", "shorts"],
    scenes=[
        S("hook", "s538935488", "Did you know you can edit photos right inside ChatGPT? No Photoshop.", title="Edit photos\ninside ChatGPT", sub="No Photoshop needed"),
        S("point", "s776951397", "Tap any image it made to open the editing tools. You can also upload your own photo and say what to change.", num="1", kicker="Where?", title="Tap the image", sub="Or upload your own photo"),
        S("grid", "s540684977", "There are four useful tools. Remove background. Eraser, for unwanted objects. Resize, for example for stories. And comment: write on the image what should change.", kicker="4 useful tools", items=[["bg", "Remove BG", "One click"], ["erase", "Eraser", "Remove extras"], ["resize", "Resize", "e.g. for stories"], ["comment", "Comment", "Say what to change"]], first=2.0),
        S("point", "s524369452", "Just remember: don't edit or share photos of other people without their permission.", mark="bad", num="!", kicker="Remember", title="Ask before editing\nother people", sub="And don't share without consent"),
        S("cta", "s519316784", "Send this to a friend who still fights with Photoshop.", title="Send this to a friend\n[[still in Photoshop]]", sub="Subscribe for more"),
    ])

V["en05_sketch"] = dict(
    tag="AI IMAGES", accent="#ff8a3d", accent2="#3ddc97", post="392979957", uuid="-7922332",
    title="From Doodle to Full Image with ChatGPT Sketch #shorts",
    desc="Can't draw? Doesn't matter. ChatGPT's Sketch feature turns a simple doodle into a full image.\n\nHow:\n1. Open Images from the menu\n2. Choose Sketch\n3. Draw your layout\n4. Describe the style you want\n\nYou decide where everything goes. Great for posters, logos and covers.",
    tags=["ChatGPT sketch", "sketch to image", "AI drawing", "ChatGPT images", "AI art", "shorts"],
    scenes=[
        S("hook", "s528181152", "Can't draw? Doesn't matter. ChatGPT turns a simple doodle into a pro image.", title="Can't draw?\n[[Doesn't matter]]", sub="ChatGPT makes it pro"),
        S("sketch", "s799936566", "It's called Sketch. Draw something simple, like a mountain and a sun, and it turns it into a full image.", kicker="The Sketch feature", cap1="Your doodle", cap2="Final image"),
        S("steps", "s718055129", "Open Images from the menu. Choose Sketch. Draw your idea. And describe the style you want.", kicker="How?", items=[["Step 1", "Open Images from the menu"], ["Step 2", "Choose Sketch"], ["Step 3", "Draw your idea"], ["Step 4", "Describe the style"]], first=0.4),
        S("point", "s540684977", "The best part: you decide where everything goes. Perfect for posters, logos and covers.", mark="good", num="★", kicker="Why it's great", title="You control\nthe layout", sub="Perfect for:", chips=["Posters", "Logos", "Covers"]),
        S("cta", "s794774811", "What would you draw first? Tell me in the comments.", title="What would you\ndraw [[first?]]", sub="Tell me in the comments"),
    ])

V["en06_video"] = dict(
    tag="AI VIDEO", accent="#ff4f9a", accent2="#5fd3ff", post="392979992", uuid="-4211246",
    title="Can ChatGPT Make Videos? The Honest Answer #shorts",
    desc="Can ChatGPT make videos? Directly, no. OpenAI's Sora video app was shut down in spring 2026.\n\nBut ChatGPT is great at 3 things:\n• Script and hook\n• Scene-by-scene storyboard\n• A prompt for every scene\n\nThen give those prompts to a video tool like Veo or Kling.",
    tags=["ChatGPT video", "AI video", "Sora", "Veo", "Kling", "AI video generator", "shorts"],
    scenes=[
        S("hook", "s524244343", "Can ChatGPT make videos? Here's the honest answer.", title="Can ChatGPT\nmake [[videos?]]", sub="The honest answer"),
        S("point", "s539514486", "Directly, no. Sora, OpenAI's video app, was shut down this spring.", mark="bad", num="!", kicker="Short answer", title="Directly? No.", sub="The Sora app shut down in spring 2026"),
        S("board", "s540699262", "But it's great at three things: it writes the script, builds a scene by scene storyboard, and writes a prompt for every scene.", kicker="But it nails these 3", items=[["Script", "Text and hook"], ["Storyboard", "Scene by scene"], ["Prompts", "One per scene"]], first=2.4),
        S("point", "s739776879", "Then you give those prompts to a video tool, like Veo or Kling.", mark="good", num="★", kicker="Last step", title="Give the prompts\nto a video tool", sub="Like Veo or Kling"),
        S("cta", "s539410140", "Next video: the video prompt formula. Subscribe so you don't miss it.", title="Next:\n[[video prompt formula]]", sub="Subscribe so you don't miss it"),
    ])

V["en07_vprompt"] = dict(
    tag="AI VIDEO", accent="#ff4f9a", accent2="#ffd23f", post="392980019", uuid="-4022450",
    title="The AI Video Prompt Formula That Works Everywhere #shorts",
    desc="A video prompt formula that works in any AI video generator.\n\n4 parts:\n1. Scene: who, where, doing what\n2. Camera move: e.g. slow zoom\n3. Light and mood: e.g. cinematic and warm\n4. Length: e.g. 5 seconds\n\nAsk ChatGPT: \"Write 3 scenes for a 15-second video about [topic], with a video prompt for each: scene, camera move, light, length.\"\n\nTip: one movement per scene.",
    tags=["AI video prompt", "video prompt formula", "Veo", "Kling", "AI video", "prompt engineering", "shorts"],
    scenes=[
        S("hook", "s739776879", "The video prompt formula that works in any AI video generator.", title="The AI video\n[[prompt formula]]", sub="Works in any video generator"),
        S("steps", "s540699262", "It has four parts. Scene: who, where, doing what. Camera move: like a slow zoom. Light and mood: like cinematic and warm. And length: like five seconds.", kicker="It has 4 parts", items=[["Scene", "Who, where, doing what"], ["Camera", "e.g. slow zoom"], ["Light & mood", "e.g. cinematic, warm"], ["Length", "e.g. 5 seconds"]], first=1.4),
        S("prompt", "s740481635", "You don't have to write it yourself. Tell ChatGPT: write three scenes for a fifteen second video about this topic, and give a video prompt for each scene.", title="Ask ChatGPT 👇", lines=["Write 3 scenes for a 15-second", "video about [[topic]].", "Give a video prompt for each:", "scene, camera, light, length."]),
        S("point", "s524244343", "Pro tip: ask for just one movement per scene. A busy prompt gives you a messy video.", mark="good", num="★", kicker="Pro tip", title="One movement\nper scene", sub="Busy prompt = messy video"),
        S("cta", "s635719043", "Save this for your first AI video.", title="Save it for your\n[[first AI video]]", sub="Subscribe for the last part"),
    ])

V["en08_img2vid"] = dict(
    tag="AI VIDEO", accent="#ff4f9a", accent2="#3ddc97", post="392980118", uuid="-5356592",
    title="Easiest Way to Make AI Video: Image First, Then Animate #shorts",
    desc="The simplest way to make an AI video: make the image first, then bring it to life.\n\n1. Create the scene image with ChatGPT\n2. Upload it to a video generator\n3. Say what should move\n\nWhy it's better: you control the look, so characters and colors don't change mid-video.\n\nKeep the motion prompt simple: \"the camera slowly zooms in and her hair moves in the wind\".",
    tags=["image to video", "AI video", "ChatGPT", "AI animation", "Kling", "Veo", "shorts"],
    scenes=[
        S("hook", "s419595292", "An easier way to make AI videos: make the image first, then bring it to life.", title="Make the image,\nthen [[bring it to life]]", sub="The easiest way to make AI video"),
        S("board", "s538935488", "Step one: create the scene image with ChatGPT. Step two: upload it to a video generator. Step three: say what should move.", kicker="3 steps", items=[["Image", "Make it in ChatGPT"], ["Upload", "To a video generator"], ["Motion", "Say what moves"]], first=0.4),
        S("point", "s524369452", "Why is this better? Because you control the look, and characters and colors don't change halfway through.", num="1", kicker="Why it's better", title="You control\nthe look", sub="Characters and colors stay consistent"),
        S("compare", "s539410140", "Keep the motion prompt simple too. For example: the camera slowly zooms in, and her hair moves in the wind.", kicker="Motion prompt", title="Keep it simple", bad="Make an epic video", good="The camera slowly zooms in and her hair moves in the wind"),
        S("cta", "s519316784", "Which part of this series helped you most? Tell me in the comments.", title="Which part\n[[helped you most?]]", sub="Tell me in the comments"),
    ])

V["en09_teacher"] = dict(
    tag="USEFUL PROMPT", accent="#ffd23f", accent2="#ff8fab", post="392980147", uuid="-5830386",
    title="Turn AI Into Your Personal Tutor (Copy This Prompt) #shorts",
    desc="Turn AI into your private tutor. Copy this prompt:\n\n\"Like a patient teacher, explain [topic] to a beginner. Step by step, with simple examples. Then ask me 3 questions.\"\n\nWhy it works: it matches your level, and it quizzes you so you know you actually learned it.\n\nStuck? Say \"explain it simpler\" or \"give me another example\".",
    tags=["AI tutor", "ChatGPT prompt", "learn with AI", "study tips", "prompt", "AI for students", "shorts"],
    scenes=[
        S("hook", "s589368520", "Turn AI into your personal tutor. It can teach you anything you want.", title="Make AI your\n[[personal tutor]]", sub="Learn anything"),
        S("prompt", "s624757079", "Write this prompt: Like a patient teacher, explain this topic to a beginner. Step by step, with simple examples. Then ask me three questions.", title="Copy this 👇", lines=["Like a patient teacher,", "explain [[topic]] to a beginner.", "Step by step, with simple examples.", "Then ask me 3 questions."]),
        S("point", "s539425946", "Why does it work? Because it matches your level. Not too easy, not too hard.", num="1", kicker="Why it works", title="It matches\nyour level", sub="Not too easy, not too hard"),
        S("point", "s774208663", "And it quizzes you, so you know if you really learned it.", num="2", kicker="Reason two", title="It quizzes you", sub="So you know you really learned it"),
        S("point", "s740481635", "And whenever you get stuck, ask it to explain simpler, or give another example.", num="3", kicker="Pro tip", title="Stuck? Just ask", sub="For example, say:", chips=["Explain it simpler", "Another example"]),
        S("cta", "s577793282", "Save this, and try it tonight.", title="Save it and\n[[try it tonight]]", sub="Subscribe for more prompts"),
    ])

V["en10_photo"] = dict(
    tag="AI TRICKS", accent="#5fd3ff", accent2="#ffd23f", post="392980186", uuid="-8911630",
    title="3 Things AI Can Do With Just One Photo #shorts",
    desc="ChatGPT and Claude understand images too. Just send a photo:\n\n1. A photo of your fridge → meal ideas with what you have\n2. A screenshot of an error → step-by-step fix\n3. A foreign restaurant menu → translation and what each dish is\n\nNever send photos of IDs, bank cards or personal documents.",
    tags=["ChatGPT vision", "AI tricks", "ChatGPT tips", "Claude", "AI hacks", "shorts"],
    scenes=[
        S("hook", "s776951397", "Did you know you can send AI just a photo, and get an answer?", title="Send a [[photo]],\nget an answer", sub="ChatGPT and Claude understand images"),
        S("io", "s866361970", "One. Snap your fridge and ask what to cook. You get meal ideas.", kicker="Trick 1", icon="fridge", inp="A photo of your fridge", out="Meal ideas with what you have"),
        S("io", "s740481635", "Two. Screenshot an error message on your phone or computer. It tells you what to do, step by step.", kicker="Trick 2", icon="error", inp="A screenshot of an error", out="A step-by-step fix"),
        S("io", "s807045794", "Three. Traveling? Snap the restaurant menu. It translates it and explains each dish.", kicker="Trick 3", icon="menu", inp="A foreign restaurant menu", out="Translation and what each dish is"),
        S("point", "s602810685", "Just remember: never send photos of your ID or bank cards.", mark="bad", num="!", kicker="Remember", title="Never send\nyour documents", sub="Bank cards · IDs · personal info"),
        S("cta", "s794774811", "What have you asked it with a photo? Tell me in the comments.", title="What did you\nask with a [[photo?]]", sub="Tell me in the comments"),
    ])

V["en11_tasks"] = dict(
    tag="PRODUCTIVITY", accent="#3ddc97", accent2="#ff8fab", post="392980221", uuid="60073077",
    title="5 Things AI Does for You in 1 Minute #shorts",
    desc="5 things AI can do for you in one minute:\n\n1. Summarize a long text: 10 pages into 5 lines\n2. Reply to emails: polite, short, professional\n3. Plan your week: list your tasks, get a schedule\n4. Translate with a natural tone, not word for word\n5. Brainstorm 10 ideas for names, captions or gifts\n\nWhich one will you try today?",
    tags=["AI productivity", "ChatGPT tips", "AI hacks", "save time", "AI tools", "shorts"],
    scenes=[
        S("hook", "s512055248", "Five things AI can do for you in one minute.", title="5 things AI does\nin [[1 minute]]", sub="Everyone needs number 5"),
        S("point", "s774208663", "One. Summarize a long text. A ten page article, in five lines.", num="1", kicker="Task 1", title="Summarize\nlong text", sub="10 pages into 5 lines"),
        S("point", "s740481635", "Two. Reply to emails. Polite, short, and professional.", num="2", kicker="Task 2", title="Reply to emails", sub="Polite, short, professional"),
        S("point", "s713180760", "Three. Plan your week. List your tasks, get a schedule.", num="3", kicker="Task 3", title="Plan your week", sub="List your tasks, get a schedule"),
        S("point", "s807045794", "Four. Translate, with a natural tone, not word for word.", num="4", kicker="Task 4", title="Translate", sub="Natural tone, not word for word"),
        S("point", "s589368520", "Five. Brainstorm. Ten ideas for names, captions, or gifts.", num="5", kicker="Task 5", title="Brainstorm", sub="10 ideas for:", chips=["Names", "Captions", "Gifts"]),
        S("cta", "s577793282", "Which one will you try today? Send this to a friend.", title="Which one will\nyou try [[today?]]", sub="Send this to a friend"),
    ])

V["en12_interview"] = dict(
    tag="CAREER HACK", accent="#ffb347", accent2="#ff6a88", post="392980259", uuid="88057522",
    title="Practice Job Interviews With AI (Copy This Prompt) #shorts",
    desc="Practice your job interview with AI, stress-free, as many times as you want.\n\nCopy this prompt:\n\"You are the interviewer for a [job title] role. Ask me questions one at a time. Give feedback after each answer. At the end, give me a score.\"\n\nTip: turn on voice mode and answer out loud, like a real interview.",
    tags=["job interview", "interview practice", "ChatGPT prompt", "career tips", "AI for jobs", "shorts"],
    scenes=[
        S("hook", "s846786123", "Before your next job interview, practice with AI. No stress, as many times as you want.", title="Practice your\njob interview\nwith [[AI]]", sub="No stress, unlimited tries"),
        S("prompt", "s740481635", "Write this: You are the interviewer for this job. Ask me questions one at a time. Give feedback after each answer. And at the end, give me a score.", title="Copy this 👇", lines=["You're the interviewer for a", "[[job title]] role.", "Ask me questions one at a time.", "Give feedback after each answer.", "At the end, give me a score."]),
        S("point", "s750974928", "Why does it work? Because it asks real questions that fit that exact job.", num="1", kicker="Why it works", title="It asks real\nquestions", sub="Tailored to that exact job"),
        S("point", "s539514486", "And it shows your weak spots, so you know where to answer better.", num="2", kicker="Reason two", title="It shows your\nweak spots", sub="So you know what to improve"),
        S("point", "s549673644", "Pro tip: turn on voice mode, and answer out loud like a real interview.", mark="good", num="★", kicker="Pro tip", title="Practice out loud", sub="Turn on voice mode in the app"),
        S("cta", "s713180760", "Send this to someone who's looking for a job.", title="Send this to someone\n[[job hunting]]", sub="Subscribe for more tips"),
    ])

V["en13_language"] = dict(
    tag="LEARN LANGUAGES", accent="#5fd3ff", accent2="#ffd23f", post="392980295", uuid="-1955133",
    title="Practice Speaking Any Language With AI, 10 Minutes a Day #shorts",
    desc="Want to speak a new language better? Talk to AI for 10 minutes a day.\n\nCopy this prompt:\n\"Have a conversation with me in [language]. Topic: [travel]. My level: [intermediate]. Correct my mistakes at the end of each message.\"\n\n1. Pick your own topic: travel, interviews, shopping\n2. It corrects your mistakes, no embarrassment\n3. Use voice mode for real speaking practice",
    tags=["learn languages", "language learning", "AI tutor", "speaking practice", "ChatGPT", "shorts"],
    scenes=[
        S("hook", "s869491647", "Want to speak a new language better? Talk to AI for ten minutes a day.", title="Speak any\n[[language]] with AI", sub="Just 10 minutes a day"),
        S("prompt", "s774208663", "Write this prompt: Have a conversation with me in this language. Tell it your topic and your level, and ask it to correct your mistakes at the end of each message.", title="Copy this 👇", lines=["Talk with me in [[Spanish]].", "Topic: [[travel]]", "My level: [[intermediate]]", "Fix my mistakes after each message."]),
        S("point", "s521601495", "One. Pick your own topic. Travel, interviews, or shopping.", num="1", kicker="Step 1", title="Pick your\nown topic", sub="Whatever you need:", chips=["Travel", "Interviews", "Shopping"]),
        S("point", "s519316784", "Two. It corrects your mistakes, with zero embarrassment.", num="2", kicker="Step 2", title="It fixes your\nmistakes", sub="Zero embarrassment"),
        S("point", "s549673644", "Three. Use voice mode, so your speaking gets stronger too.", num="3", kicker="Step 3", title="Practice\nout loud", sub="Voice mode = real conversation"),
        S("cta", "s577793282", "Save this, and start today.", title="Start\n[[today]]", sub="Save it · Subscribe"),
    ])

V["en14_phrases"] = dict(
    tag="AI TRICKS", accent="#c9a7ff", accent2="#ff8fab", post="392980347", uuid="39712287",
    title="3 Phrases That Make ChatGPT's Answers Way Better #shorts",
    desc="3 phrases that make any AI answer much better:\n\n1. \"Ask me questions before you answer\" so it knows exactly what you want\n2. \"Explain step by step\" for complex problems\n3. \"Tell me the weak points of your answer\" so it critiques and improves itself\n\nExample: instead of \"give me a workout plan\", say \"give me a workout plan, but ask me questions first\".",
    tags=["ChatGPT tips", "prompt tips", "prompt engineering", "AI tricks", "better prompts", "shorts"],
    scenes=[
        S("hook", "s539514486", "Three phrases that make AI answers way better.", title="3 phrases that make\nAI answers [[way better]]", sub="Few people know number 3"),
        S("point", "s1785822976", "One. Ask me questions before you answer. That way it knows exactly what you want.", num="1", kicker="Phrase 1", title="\"Ask me questions\nbefore you answer\"", sub="So it knows exactly what you want"),
        S("point", "s720437119", "Two. Explain step by step. Great for complex problems.", num="2", kicker="Phrase 2", title="\"Explain it\nstep by step\"", sub="For complex problems"),
        S("point", "s615849265", "Three. Tell me the weak points of your answer. That way it critiques its own answer and makes it better.", num="3", kicker="Phrase 3", title="\"What are the weak\npoints of your answer?\"", sub="It critiques and improves itself"),
        S("compare", "s522000975", "For example, instead of just saying give me a workout plan, add: ask me questions first.", kicker="Example", title="Before and after", bad="Give me a workout plan", good="Give me a workout plan. Ask me questions first."),
        S("cta", "s776951397", "Which one will you try first? Tell me in the comments.", title="Which one will\nyou try [[first?]]", sub="Comment · Save"),
    ])

V["en15_dont"] = dict(
    tag="WARNING", accent="#3ddc97", accent2="#ff8fab", post="392980383", uuid="-3523643",
    title="3 Things You Shouldn't Hand Over to AI #shorts",
    desc="3 things you shouldn't fully hand over to AI:\n\n1. Medical diagnosis: fine for general info, but diagnosis and treatment belong to a doctor\n2. Big financial or legal decisions: talk to an expert first\n3. Confidential work data: no contracts, passwords or customer data in chats\n\nInstead: use AI to prepare your questions, then talk to the expert.",
    tags=["AI safety", "AI privacy", "ChatGPT tips", "AI mistakes", "artificial intelligence", "shorts"],
    scenes=[
        S("hook", "s589368520", "Three things you should never fully hand over to AI.", title="3 things you shouldn't\n[[hand over]] to AI", sub="Lots of people do number 3"),
        S("point", "s1153554736", "One. Medical diagnosis. It's fine for general info, but diagnosis and treatment belong to a doctor.", mark="bad", num="1", kicker="Thing 1", title="Medical diagnosis", sub="General info, yes. Diagnosis: a doctor."),
        S("point", "s804020665", "Two. Big financial and legal decisions. Always talk to an expert first.", mark="bad", num="2", kicker="Thing 2", title="Big money and\nlegal decisions", sub="Talk to an expert first"),
        S("point", "s740481635", "Three. Confidential work data. Don't paste contracts, passwords, or customer data into a chat.", mark="bad", num="3", kicker="Thing 3", title="Confidential\nwork data", sub="Never paste:", chips=["Contracts", "Passwords", "Customer data"]),
        S("point", "s539514486", "Instead, use it to prepare your questions, then talk to the expert.", mark="good", num="✓", kicker="Instead", title="Use it to\nprepare", sub="Get your questions ready, then ask an expert"),
        S("cta", "s615849265", "Send this to someone who asks AI about everything.", title="Send this to someone\nwho asks AI [[everything]]", sub="Subscribe for more tips"),
    ])

V["en16_caption"] = dict(
    tag="CONTENT CREATION", accent="#3ddc97", accent2="#ffd23f", post="392980419", uuid="65608253",
    title="Write Instagram Captions With AI (Copy This Prompt) #shorts",
    desc="Let AI write your Instagram captions with this prompt:\n\n\"Write an Instagram caption about [your post topic]. Friendly tone, 5 lines max. End with a question. Give 5 relevant hashtags.\"\n\n• The question at the end brings comments, and comments mean more engagement\n• Ask for 3 versions and pick the best\n• Keep your own voice: the caption should sound like you",
    tags=["Instagram captions", "AI captions", "ChatGPT prompt", "content creation", "social media tips", "shorts"],
    scenes=[
        S("hook", "s539410140", "Let AI write your Instagram captions. With just this one prompt.", title="Let AI write your\n[[Instagram captions]]", sub="With this one prompt"),
        S("prompt", "s776951397", "Write: Write an Instagram caption about my post topic. Friendly tone, five lines max. End with a question, and give five relevant hashtags.", title="Copy this 👇", lines=["Write an Instagram caption about", "[[your post topic]].", "Friendly tone, 5 lines max.", "End with a question.", "Give 5 relevant hashtags."]),
        S("point", "s635719043", "Why a question? Because a question at the end brings comments, and comments mean more engagement.", num="1", kicker="Why a question?", title="A question gets\ncomments", sub="Comments = more engagement"),
        S("point", "s1785822976", "Pro tip: ask for three versions, and pick the best one.", num="2", kicker="Pro tip", title="Ask for\n3 versions", sub="Pick the best one"),
        S("point", "s720437119", "Just remember, keep your own voice. The caption should sound like you.", num="3", kicker="Remember", title="Keep your\nown voice", sub="It should sound like you"),
        S("cta", "s519316784", "Save this, and try it on your next post.", title="Save it for your\n[[next post]]", sub="Subscribe for more tips"),
    ])

V["en17_decide"] = dict(
    tag="DECISIONS", accent="#3ddc97", accent2="#5fd3ff", post="392980449", uuid="25498630",
    title="Stuck Between Two Choices? Try This AI Prompt #shorts",
    desc="Stuck between two choices? Let AI help you decide.\n\nCopy this prompt:\n\"I'm torn between [A] and [B]. Make a table of the pros and cons of each. Then ask me 3 questions that help me decide.\"\n\nExample: two job offers → a comparison table plus 3 key questions.\n\nThe final decision is yours. AI just helps you think clearly.",
    tags=["decision making", "ChatGPT prompt", "AI tips", "pros and cons", "productivity", "shorts"],
    scenes=[
        S("hook", "s539514486", "Stuck between two choices? AI can help you decide.", title="Stuck between\n[[two choices?]]", sub="AI can help"),
        S("prompt", "s774208663", "Write: I'm torn between these two. Make a table of the pros and cons of each. Then ask me three questions that help me decide.", title="Copy this 👇", lines=["I'm torn between [[A]] and [[B]].", "Table the pros and cons of each.", "Then ask me 3 questions", "that help me decide."]),
        S("io", "s750974928", "For example, you have two job offers. You get a comparison table, plus three key questions.", kicker="Example", icon="menu", inp="Two job offers", out="Comparison table + 3 key questions"),
        S("point", "s615849265", "But the final call is yours. AI just helps you think clearly.", mark="good", num="★", kicker="Remember", title="The final call\nis yours", sub="AI just organizes your thinking"),
        S("cta", "s577793282", "What are you torn between right now? Tell me in the comments.", title="What are you\ntorn [[between?]]", sub="Tell me in the comments"),
    ])

V["en18_resume"] = dict(
    tag="CAREER HACK", accent="#b07cff", accent2="#5fd3ff", post="392980488", uuid="-1716204",
    title="Let AI Roast Your Resume Before a Recruiter Does #shorts",
    desc="Before you send your resume, let AI critique it.\n\nCopy this prompt:\n\"Like a strict hiring manager, critique my resume for a [job title] role. List 3 weak points and give a suggestion for each.\"\n\nWhy strict? No fake praise, real feedback before you get rejected.\n\nExample: instead of \"I was in charge of sales\", write the result with a number: \"Grew team sales 30% in 6 months\".\n\nRemove your phone number and address before pasting.",
    tags=["resume tips", "AI resume", "ChatGPT prompt", "job search", "career tips", "shorts"],
    scenes=[
        S("hook", "s685769725", "Before you send your resume, let AI critique it.", title="Let AI\n[[roast]] your\nresume", sub="Before a recruiter sees it"),
        S("prompt", "s718055129", "Write: Like a strict hiring manager, critique my resume for this job. List three weak points, and give a suggestion for each.", title="Copy this 👇", lines=["Like a [[strict]] hiring manager,", "critique my resume for a", "[[job title]] role.", "List 3 weak points,", "with a suggestion for each."]),
        S("point", "s518573488", "Why strict? Because you won't get fake praise. You get real feedback, before you get rejected.", num="1", kicker="Why strict?", title="No fake praise", sub="Real feedback before a rejection"),
        S("compare", "s511664824", "For example, instead of: I was in charge of sales, it suggests you write the result, with a number.", kicker="Example", title="Before and after", bad="I was in charge of sales", good="Grew team sales 30% in 6 months"),
        S("point", "s619849758", "Just one thing: remove your phone number and address first.", mark="bad", num="!", kicker="Remember", title="Remove your\ncontact info", sub="Delete phone and address before pasting"),
        S("cta", "s846786123", "Send this to someone who's looking for a job.", title="Send this to someone\n[[job hunting]]", sub="Subscribe for more tips"),
    ])

V["en19_skill"] = dict(
    tag="LEARNING", accent="#b07cff", accent2="#ffd23f", post="392980576", uuid="-2375371",
    title="Learn Any Skill in 30 Days With an AI Plan #shorts",
    desc="Want to learn a new skill? AI can build you a 30-day plan.\n\nCopy this prompt:\n\"Write a 30-day plan to learn [skill]. I have 30 minutes a day. Include one hands-on exercise every day.\"\n\nExample, phone photography:\nWeek 1: light and framing\nWeek 2: camera settings\nWeek 3: editing\nWeek 4: a full project\n\nTip: report back every night so it adjusts the plan to your pace.",
    tags=["learn new skills", "30 day challenge", "AI learning", "ChatGPT prompt", "self improvement", "shorts"],
    scenes=[
        S("hook", "s1785822976", "Want to learn any skill? AI can build you a thirty day plan.", title="Start any skill\nin [[30 days]]", sub="With a plan from AI"),
        S("prompt", "s740481635", "Write: Make a thirty day plan to learn this skill. I have thirty minutes a day. Add one hands-on exercise every day.", title="Copy this 👇", lines=["Write a 30-day plan to learn", "[[skill name]].", "I have 30 minutes a day.", "One hands-on exercise per day."]),
        S("steps", "s550108264", "For example, phone photography: week one, light and framing. Week two, camera settings. Week three, editing. And the last week, a full project.", kicker="Example: phone photography", items=[["Week 1", "Light and framing"], ["Week 2", "Camera settings"], ["Week 3", "Photo editing"], ["Week 4", "A full project"]]),
        S("point", "s720437119", "Pro tip: every night, tell it what you learned, so it adjusts the plan to your pace.", mark="good", num="★", kicker="Pro tip", title="Report back\nevery night", sub="It adjusts the plan to your pace"),
        S("cta", "s794774811", "What do you want to learn? Tell me in the comments.", title="What do you want\nto [[learn?]]", sub="Tell me in the comments"),
    ])

V["en20_no"] = dict(
    tag="COMMUNICATION", accent="#b07cff", accent2="#ff8fab", post="392980608", uuid="-3634242",
    title="Hard to Say No? Let AI Write It for You #shorts",
    desc="Saying no is hard? Let AI help.\n\nCopy this prompt:\n\"I want to tell my [coworker] I can't do [this task]. Write a respectful but firm message. 2 versions: formal and friendly.\"\n\nInstead of \"I can't, I'm busy\" you get: \"Thanks for thinking of me. I can't this week, but I'd be happy to help next week.\"\n\nWorks for emails, messages, even practicing before a tough call.",
    tags=["how to say no", "communication skills", "ChatGPT prompt", "work tips", "AI tips", "shorts"],
    scenes=[
        S("hook", "s539514486", "Saying no is hard? Let AI handle it.", title="Hard to say \"no\"?\nLet [[AI]] help", sub="Polite, but firm"),
        S("prompt", "s619849758", "Write: I want to tell my coworker I can't do this task. Write a respectful but firm message. Two versions, formal and friendly.", title="Copy this 👇", lines=["I want to tell my [[coworker]]", "I can't do [[this task]].", "Write a respectful but firm message.", "2 versions: formal and friendly."]),
        S("compare", "s750974928", "Instead of: I can't, I'm busy, you get a reply that's respectful, and doesn't hurt the relationship.", kicker="Before and after", title="See the difference", bad="I can't, I'm busy.", good="Thanks for thinking of me! I can't this week, but I'd love to help next week."),
        S("point", "s549673644", "It works for emails and messages. You can even practice before a tough call.", num="1", kicker="Use it everywhere", title="Emails, messages,\neven calls", sub="Practice before a tough call"),
        S("cta", "s521601495", "Send this to someone who can't say no.", title="Send this to someone\nwho can't say [[no]]", sub="Subscribe for more tips"),
    ])

for k, v in V.items():
    v["lang"] = "en"
    v["voice_text"] = " ".join(s["voice"] for s in v["scenes"])
    v["desc"] = v["desc"] + FOOT + "\n\n#AI #ArtificialIntelligence #AITips #shorts"

json.dump(V, open("/home/claude/reels/scripts_en.json", "w"), ensure_ascii=False, indent=1)
for k, v in V.items():
    print(k, len(v["voice_text"]), len(v["title"]))
print("total chars", sum(len(v["voice_text"]) for v in V.values()))
