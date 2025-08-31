from flask import Flask, request, redirect, url_for, render_template_string, jsonify

app = Flask(__name__)

user = {
    "name": "Player1",
    "level": 1,
    "exp": 0,
    "next_level": 100,
    "points": 0  
}

level_names = [
    "Novice", "Explorer", "Adventurer", "Warrior",
    "Knight", "Hero", "Champion", "Master", "Legend",
    "Cyber Lord", "Neon Samurai", "Glitch Hunter", "Digital Overlord"
]

tasks = {
    "Math": {
        "Quick math": {"xp": 20, "points": 10, "level_req": 2}
    },
    "One Word Type": {
        "Type 'HabitQuest' 3 times": {"xp": 10, "points": 5, "level_req": 1}
    },
    "Identify Color": {
        "Identify the color": {"xp": 15, "points": 5, "level_req": 1}
    }
}


habits = {
    "Drink Water": {"xp": 10, "points": 5, "duration": 5, "level_req": 1},
    "Meditate": {"xp": 15, "points": 10, "duration": 10, "level_req": 2},
    "Walk 2000 steps": {"xp": 20, "points": 10, "duration": 10, "level_req": 1},
    "Read a book": {"xp": 20, "points": 10, "duration": 15, "level_req": 2},
    "Clean your room": {"xp": 15, "points": 5, "duration": 10, "level_req": 1},
    "Do 5 push-ups": {"xp": 15, "points": 5, "duration": 5, "level_req": 1},
    "Write a journal": {"xp": 15, "points": 5, "duration": 10, "level_req": 1},
    "Step outside": {"xp": 10, "points": 5, "duration": 3, "level_req": 1}
}


shop_items = {
    "Fortnite Points": {"price": 50},
    "COD Points": {"price": 75},
    "Google Play Credit": {"price": 100},
    "Netflix Subscription": {"price": 200},
    "Prime Subscription": {"price": 200}
}



def add_exp(amount):
    user["exp"] += amount
    while user["exp"] >= user["next_level"]:
        user["exp"] -= user["next_level"]
        user["level"] += 1
        user["next_level"] = int(user["next_level"] * 1.5)

def complete_task_or_habit(xp, points):
    add_exp(xp)
    user["points"] += points

def buy_item(item):
    if item in shop_items:
        cost = shop_items[item]["price"]
        if user["points"] >= cost:
            user["points"] -= cost
            return True
    return False

@app.route("/")
def home():
    return render_template_string(home_template, user=user, level_names=level_names)




@app.route("/daily")
def daily():
    return render_template_string(daily_template, user=user, habits=habits, level_names=level_names)

@app.route("/tasks")
def task_page():
    return render_template_string(task_template, user=user, tasks=tasks, level_names=level_names)


@app.route("/shop")
def shop():
    return render_template_string(shop_template, user=user, shop_items=shop_items)


@app.route("/complete_habit/<habit>")
def complete_habit(habit):
    if habit in habits:
        habit_data = habits[habit]
        if user["level"] >= habit_data["level_req"]:
            complete_task_or_habit(habit_data["xp"], habit_data["points"])
    return redirect(url_for("daily"))


@app.route("/complete_task/<category>/<task>")
def complete_task(category, task):
    if category in tasks and task in tasks[category]:
        task_data = tasks[category][task]
        if user["level"] >= task_data["level_req"]:
            complete_task_or_habit(task_data["xp"], task_data["points"])
    return redirect(url_for("task_page"))

@app.route("/buy/<item>")
def buy(item):
    buy_item(item)
    return redirect(url_for("shop"))

@app.route("/complete_habit_ajax", methods=["POST"])
def complete_habit_ajax():
    data = request.get_json()
    xp = data.get("xp", 0)
    points = data.get("points", 0)
    user["exp"] += xp
    user["points"] += points
    while user["exp"] >= user["next_level"]:
        user["exp"] -= user["next_level"]
        user["level"] += 1
        user["next_level"] = int(user["next_level"] * 1.5)
    return jsonify({"status": "ok", "exp": user["exp"], "points": user["points"], "level": user["level"]})


@app.route("/complete_task_ajax", methods=["POST"])
def complete_task_ajax():
    data = request.get_json()
    xp = data.get("xp", 0)
    points = data.get("points", 0)
    user["exp"] += xp
    user["points"] += points
    while user["exp"] >= user["next_level"]:
        user["exp"] -= user["next_level"]
        user["level"] += 1
        user["next_level"] = int(user["next_level"] * 1.5)
    return jsonify({"status": "ok", "exp": user["exp"], "points": user["points"], "level": user["level"]})


@app.route("/buy_item_ajax", methods=["POST"])
def buy_item_ajax():
    data = request.get_json()
    price = data.get("price", 0)
    if user["points"] >= price:
        user["points"] -= price
        return jsonify({"status": "ok", "points": user["points"]})
    else:
        return jsonify({"status": "fail", "points": user["points"]})




home_template = """
<!DOCTYPE html>
<html>
<head>
    <title>⚡ HabitQuest Home ⚡</title>
    <style>
        .left-panel {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            grid-auto-rows: 120px; /* rectangle height */
            gap: 15px;
        }
        .task-card, .habit-card, .shop-card {
            background: linear-gradient(45deg,#8e2de2,#4a00e0);
            color: white;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.3s;
            padding: 10px;
            font-weight: bold;
        }
        .task-card:hover, .habit-card:hover, .shop-card:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px #ff6ec7;
        }        
        body { font-family: 'Orbitron', sans-serif; background: #0a0a23; color: #e0c3fc; text-align: center; padding: 30px; }
        .nav { margin: 20px; }
        .nav a { display: inline-block; margin: 0 10px; padding: 10px 20px; background: linear-gradient(45deg,#8e2de2,#4a00e0); border-radius: 12px; text-decoration: none; color: white; font-weight: bold; }
        .nav a:hover { transform: scale(1.05); box-shadow: 0 0 15px #8e2de2,0 0 25px #4a00e0; }
        .gauge { width: 60%; margin: 20px auto; background: #222244; border-radius: 20px; overflow: hidden; height: 25px; }
        .gauge-bar { height: 25px; background: linear-gradient(90deg,#8e2de2,#4a00e0); width: {{ (user['exp']/user['next_level'])*100 }}%; transition: width 0.5s; }
        .points-bar { height: 25px; background: linear-gradient(90deg,#ff6ec7,#e0c3fc); width: {{ (user['points']/500)*100 if user['points']<500 else 100 }}%; transition: width 0.5s; }
    </style>
</head>
<body>
    <h1>Welcome to ⚡ HabitQuest ⚡</h1>
    <p>Hi {{ user['name'] }}! Level {{ user['level'] }} ({{ level_names[user['level']-1] if user['level']-1 < level_names|length else "Neon Mythic" }})</p>
    
    <p>EXP: {{ user['exp'] }} / {{ user['next_level'] }}</p>
    <div class="gauge"><div class="gauge-bar"></div></div>
    
    <p>Points: {{ user['points'] }}</p>
    <div class="gauge"><div class="points-bar"></div></div>
    
    <div class="nav">
        <a href="{{ url_for('daily') }}">Daily Habits</a>
        <a href="{{ url_for('task_page') }}">Tasks</a>
        <a href="{{ url_for('shop') }}">Shop</a>
    </div>
</body>
</html>
"""


daily_template = """
<!DOCTYPE html>
<html>
<head>
    <title>HabitQuest Daily Habits</title>
    <style>
        .left-panel {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            grid-auto-rows: 120px; /* rectangle height */
            gap: 15px;
        }
        .task-card, .habit-card, .shop-card {
            background: linear-gradient(45deg,#8e2de2,#4a00e0);
            color: white;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.3s;
            padding: 10px;
            font-weight: bold;
        }
        .task-card:hover, .habit-card:hover, .shop-card:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px #ff6ec7;
        }
        body { font-family: 'Orbitron', sans-serif; background: #0a0a23; color: #e0c3fc; margin: 0; padding: 0; display: flex; height: 100vh; }
        .left-panel { width: 70%; padding: 20px; display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; overflow-y: auto; }
        .habit-card { background: linear-gradient(45deg,#8e2de2,#4a00e0); padding: 15px; border-radius: 15px; color: white; text-align: center; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.3s; font-weight: bold; }
        .habit-card:hover { transform: scale(1.05); box-shadow: 0 0 15px #ff6ec7; }
        .right-panel { width: 30%; padding: 20px; background: #111133; display: flex; flex-direction: column; align-items: center; box-shadow: 0 0 20px #8e2de2; }
        .gauge { width: 90%; background: #222244; border-radius: 20px; overflow: hidden; height: 25px; margin: 10px 0; }
        .gauge-bar { height: 25px; background: linear-gradient(90deg,#8e2de2,#4a00e0); width: {{ (user['exp']/user['next_level'])*100 }}%; transition: width 0.5s; }
        .points-bar { height: 25px; background: linear-gradient(90deg,#ff6ec7,#e0c3fc); width: {{ (user['points']/500)*100 if user['points']<500 else 100 }}%; transition: width 0.5s; }
        button { padding: 10px 20px; border-radius: 12px; border: none; font-weight: bold; background: #e0c3fc; color: black; margin: 10px 0; cursor: pointer; width: 80%; }
        button:hover { background: #ff6ec7; color: white; }
        #game-area { width: 90%; margin-top: 20px; text-align:center; }
    </style>
</head>
<body>
    <div class="left-panel">
        {% for habit, data in habits.items() %}
            {% if user['level'] >= data['level_req'] %}
                <div class="habit-card" onclick="completeHabit('{{ habit }}', {{ data['xp'] }}, {{ data['points'] }})">
                    <strong>{{ habit }}</strong><br>
                    Duration: {{ data['duration'] }} min<br>
                    +{{ data['xp'] }} EXP, +{{ data['points'] }} Points
                </div>
            {% else %}
                <div class="habit-card" style="opacity:0.5; cursor:not-allowed;">
                    <strong>{{ habit }}</strong><br>Unlocks at Level {{ data['level_req'] }}
                </div>
            {% endif %}
        {% endfor %}
    </div>

    <div class="right-panel">
        <h2>{{ user['name'] }}</h2>
        <p>Level {{ user['level'] }} / {{ level_names[user['level']-1] if user['level']-1 < level_names|length else 'Neon Mythic' }}</p>
        <p>EXP: {{ user['exp'] }} / {{ user['next_level'] }}</p>
        <div class="gauge"><div class="gauge-bar" id="exp-bar"></div></div>
        <p>Points: {{ user['points'] }}</p>
        <div class="gauge"><div class="points-bar" id="points-bar"></div></div>

        <button onclick="location.href='{{ url_for('home') }}'">Home</button>
        <button onclick="location.href='{{ url_for('task_page') }}'">Tasks</button>
        <button onclick="location.href='{{ url_for('shop') }}'">Shop</button>

        <div id="game-area">
            <p>Select a habit from the left to complete</p>
        </div>
    </div>

<script>
function completeHabit(habit, xp, points){
    fetch("/complete_habit_ajax", {
        method:"POST",
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({xp: xp, points: points})
    }).then(res=>res.json()).then(data=>{
        document.getElementById("game-area").innerHTML = "<p style='color:#0ff;'>Habit Completed: +" + xp + " EXP, +" + points + " Points</p>";
        document.getElementById("exp-bar").style.width = (data.exp/{{ user['next_level'] }}*100)+"%";
        document.getElementById("points-bar").style.width = (data.points/500*100>100?100:(data.points/500*100))+"%";
    });
}

</script>
</body>
</html>
"""



task_template = """
<!DOCTYPE html>
<html>
<head>
    <title>⚡ HabitQuest Tasks ⚡</title>
    <style>
        .left-panel {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            grid-auto-rows: 120px; /* rectangle height */
            gap: 15px;
        }
        .task-card, .habit-card, .shop-card {
            background: linear-gradient(45deg,#8e2de2,#4a00e0);
            color: white;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.3s;
            padding: 10px;
            font-weight: bold;
        }
        .task-card:hover, .habit-card:hover, .shop-card:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px #ff6ec7;
        }
        body { font-family: 'Orbitron', sans-serif; background: #0a0a23; color: #e0c3fc; margin: 0; padding: 0; display: flex; height: 100vh; }
        .left-panel { width: 70%; padding: 20px; display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; overflow-y: auto; }
        .habit-card { background: linear-gradient(45deg,#8e2de2,#4a00e0); padding: 15px; border-radius: 15px; color: white; text-align: center; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.3s; font-weight: bold; }
        .habit-card:hover { transform: scale(1.05); box-shadow: 0 0 15px #ff6ec7; }
        .right-panel { width: 30%; padding: 20px; background: #111133; display: flex; flex-direction: column; align-items: center; box-shadow: 0 0 20px #8e2de2; }
        .gauge { width: 90%; background: #222244; border-radius: 20px; overflow: hidden; height: 25px; margin: 10px 0; }
        .gauge-bar { height: 25px; background: linear-gradient(90deg,#8e2de2,#4a00e0); width: {{ (user['exp']/user['next_level'])*100 }}%; transition: width 0.5s; }
        .points-bar { height: 25px; background: linear-gradient(90deg,#ff6ec7,#e0c3fc); width: {{ (user['points']/500)*100 if user['points']<500 else 100 }}%; transition: width 0.5s; }
        button { padding: 10px 20px; border-radius: 12px; border: none; font-weight: bold; background: #e0c3fc; color: black; margin: 10px 0; cursor: pointer; width: 80%; }
        button:hover { background: #ff6ec7; color: white; }
        #game-area { width: 90%; margin-top: 20px; text-align:center; }
    </style>
</head>
<body>
    <div class="left-panel">
        {% for category, cat_tasks in tasks.items() %}
            {% for task, data in cat_tasks.items() %}
                {% if user['level'] >= data['level_req'] %}
                    <div class="task-card" onclick="startTask('{{ category }}','{{ task }}', {{ data['xp'] }}, {{ data['points'] }})">
                        <strong>{{ task }}</strong><br>
                        (+{{ data['xp'] }} EXP, +{{ data['points'] }} Points)
                    </div>
                {% else %}
                    <div class="task-card" style="opacity:0.5;">
                        <strong>{{ task }}</strong><br>Unlocks at Level {{ data['level_req'] }}
                    </div>
                {% endif %}
            {% endfor %}
        {% endfor %}
    </div>

    <div class="right-panel">
        <h2>{{ user['name'] }}</h2>
        <p>Level {{ user['level'] }} / {{ level_names[user['level']-1] if user['level']-1 < level_names|length else 'Neon Mythic' }}</p>
        <p>EXP: {{ user['exp'] }} / {{ user['next_level'] }}</p>
        <div class="gauge"><div class="gauge-bar" id="exp-bar"></div></div>
        <p>Points: {{ user['points'] }}</p>
        <div class="gauge"><div class="points-bar" id="points-bar"></div></div>

        <button onclick="location.href='{{ url_for('home') }}'">Home</button>
        <button onclick="location.href='{{ url_for('daily') }}'">Daily Habits</button>
        <button onclick="location.href='{{ url_for('shop') }}'">Shop</button>

        <div id="game-area">
            <p>Select a task from the left to start</p>
        </div>
    </div>

<script>
let currentTask = null;

function startTask(category, task, xp, points){
    currentTask = {category, task, xp, points};
    let gameArea = document.getElementById("game-area");
    gameArea.innerHTML = "";

    if(category === "Math"){
        let question = document.createElement("p");
        question.textContent = "Solve: " + task;
        let input = document.createElement("input"); input.type="text"; input.placeholder="Enter answer";
        let btn = document.createElement("button"); btn.textContent="Submit"; btn.onclick=()=>checkMath(input.value);
        gameArea.append(question,input,btn);

    } else if(category === "Quick Math"){
        let num1 = Math.floor(Math.random() * 20) + 1;
        let num2 = Math.floor(Math.random() * 20) + 1;
        let operators = ["+","-","*"];
        let op = operators[Math.floor(Math.random() * operators.length)];
        let questionText = `${num1} ${op} ${num2}`;
        currentTask.answer = eval(questionText);
        let question = document.createElement("p"); question.textContent="Solve: " + questionText;
        let input = document.createElement("input"); input.type="text"; input.placeholder="Enter answer";
        let btn = document.createElement("button"); btn.textContent="Submit"; btn.onclick=()=>checkMath(input.value);
        gameArea.append(question,input,btn);

    } else if(category === "One Word Type"){
        let question = document.createElement("p"); question.textContent="Type exactly: " + task;
        let input = document.createElement("input"); input.type="text"; input.placeholder="Type here";
        let btn = document.createElement("button"); btn.textContent="Submit"; btn.onclick=()=>checkType(input.value);
        gameArea.append(question,input,btn);

    } else if(category === "Identify Color"){
        let question = document.createElement("p"); question.textContent="Identify the color: (e.g., 'blue')";
        let colorBox = document.createElement("div"); colorBox.style.width="100px"; colorBox.style.height="50px"; colorBox.style.backgroundColor="blue"; colorBox.style.margin="10px auto";
        let input = document.createElement("input"); input.type="text"; input.placeholder="Enter color name";
        let btn = document.createElement("button"); btn.textContent="Submit"; btn.onclick=()=>checkColor(input.value);
        gameArea.append(question,colorBox,input,btn);

    } else if(category === "Captcha"){
        let captchaText = task.split(":")[1].trim();
        let question = document.createElement("p"); question.textContent="Enter the captcha: " + captchaText;
        let input = document.createElement("input"); input.type="text"; input.placeholder="Type captcha here";
        let btn = document.createElement("button"); btn.textContent="Submit"; btn.onclick=()=>checkCaptcha(input.value,captchaText);
        gameArea.append(question,input,btn);
    }
}

function updateBars(exp, points){
    document.getElementById("exp-bar").style.width = (exp/{{ user['next_level'] }}*100)+"%";
    document.getElementById("points-bar").style.width = (points/500*100>100?100:(points/500*100))+"%";
}

function completeSuccess(){
    fetch("/complete_task_ajax", {
        method:"POST",
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({xp: currentTask.xp, points: currentTask.points})
    }).then(res=>res.json()).then(data=>{
        updateBars(data.exp,data.points);
        document.getElementById("game-area").innerHTML = "<p class='message' style='color:#0ff;'>Task Completed! +" + currentTask.xp + " EXP, +" + currentTask.points + " Points</p>";
    });
}

function checkMath(value){ if(parseInt(value)===currentTask.answer){ completeSuccess(); } else { alert("Incorrect, try again!"); } }
function checkType(value){ if(value.trim()===currentTask.task){ completeSuccess(); } else { alert("Incorrect, try again!"); } }
function checkColor(value){ if(value.toLowerCase()==="blue"){ completeSuccess(); } else { alert("Incorrect, try again!"); } }
function checkCaptcha(value,captchaText){ if(value.trim()===captchaText){ completeSuccess(); } else { alert("Incorrect, try again!"); } }
</script>
</body>
</html>


"""

shop_template = """
<!DOCTYPE html>
<html>
<head>
    <title>HabitQuest Shop</title>
    <style>
        .left-panel {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            grid-auto-rows: 120px; /* rectangle height */
            gap: 15px;
        }
        .task-card, .habit-card, .shop-card {
            background: linear-gradient(45deg,#8e2de2,#4a00e0);
            color: white;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.3s;
            padding: 10px;
            font-weight: bold;
        }
        .task-card:hover, .habit-card:hover, .shop-card:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px #ff6ec7;
        }
        body { font-family: 'Orbitron', sans-serif; background: #0a0a23; color: #e0c3fc; margin: 0; padding: 0; display: flex; height: 100vh; }
        .left-panel { width: 70%; padding: 20px; display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; overflow-y: auto; }
        .shop-card { background: linear-gradient(45deg,#8e2de2,#4a00e0); padding: 15px; border-radius: 15px; color: white; text-align: center; cursor: pointer; transition: 0.3s; font-weight: bold; display: flex; align-items: center; justify-content: center; }
        .shop-card:hover { transform: scale(1.05); box-shadow: 0 0 15px #ff6ec7; }
        .right-panel { width: 30%; padding: 20px; background: #111133; display: flex; flex-direction: column; align-items: center; box-shadow: 0 0 20px #8e2de2; }
        .gauge { width: 90%; background: #222244; border-radius: 20px; overflow: hidden; height: 25px; margin: 10px 0; }
        .points-bar { height: 25px; background: linear-gradient(90deg,#ff6ec7,#e0c3fc); width: {{ (user['points']/500)*100 if user['points']<500 else 100 }}%; transition: width 0.5s; }
        button { padding: 10px 20px; border-radius: 12px; border: none; font-weight: bold; background: #e0c3fc; color: black; margin: 10px 0; cursor: pointer; width: 80%; }
        button:hover { background: #ff6ec7; color: white; }
        #shop-msg { margin-top:20px; font-weight:bold; text-align:center; }
    </style>
</head>
<body>
    <div class="left-panel">
        {% for item, data in shop_items.items() %}
            {% if user['points'] >= data.price %}
                <div class="shop-card" onclick="buyItem('{{ item }}', {{ data.price }})">
                    <strong>{{ item }}</strong><br>
                    Price: {{ data.price }} Points
                </div>
            {% else %}
                <div class="shop-card" style="opacity:0.5; cursor:not-allowed;">
                    <strong>{{ item }}</strong><br>
                    Price: {{ data.price }} Points
                </div>
            {% endif %}
        {% endfor %}
    </div>

    <div class="right-panel">
        <h2>{{ user['name'] }}</h2>
        <p>Points: {{ user['points'] }}</p>
        <div class="gauge"><div class="points-bar" id="points-bar"></div></div>

        <button onclick="location.href='{{ url_for('home') }}'">Home</button>
        <button onclick="location.href='{{ url_for('daily') }}'">Daily Habits</button>
        <button onclick="location.href='{{ url_for('task_page') }}'">Tasks</button>

        <div id="shop-msg"></div>
    </div>

<script>
function buyItem(item, price){
    if(confirm("Buy " + item + " for " + price + " points?")){
        fetch("/buy_item_ajax", {
            method:"POST",
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({price: price})
        }).then(res=>res.json()).then(data=>{
            if(data.status === "ok"){
                document.getElementById("points-bar").style.width = (data.points/500*100>100?100:(data.points/500*100))+"%";
                document.getElementById("shop-msg").innerHTML = "<p style='color:#0ff;'>Purchased " + item + "!</p>";
            } else {
                document.getElementById("shop-msg").innerHTML = "<p style='color:#f00;'>Not enough points!</p>";
            }
        });
    }
}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
