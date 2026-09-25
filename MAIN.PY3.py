from ursina import *

app = Ursina()

# ==========================================
# إعدادات اللعبة
# ==========================================

window.title = "My 3D Adventure"
window.borderless = False
window.color = color.rgb(30, 30, 40)

# ==========================================
# الأرض
# ==========================================

ground = Entity(
    model='cube',
    scale=(30, 1, 30),
    position=(0, -0.5, 0),
    color=color.rgb(70, 120, 70),
    collider='box'
)

# ==========================================
# الجدران
# ==========================================

wall1 = Entity(
    model='cube',
    scale=(30, 4, 1),
    position=(0, 2, 15),
    color=color.rgb(100, 100, 110),
    collider='box'
)

wall2 = Entity(
    model='cube',
    scale=(30, 4, 1),
    position=(0, 2, -15),
    color=color.rgb(100, 100, 110),
    collider='box'
)

wall3 = Entity(
    model='cube',
    scale=(1, 4, 30),
    position=(15, 2, 0),
    color=color.rgb(100, 100, 110),
    collider='box'
)

wall4 = Entity(
    model='cube',
    scale=(1, 4, 30),
    position=(-15, 2, 0),
    color=color.rgb(100, 100, 110),
    collider='box'
)

# ==========================================
# الأشجار
# ==========================================

def create_tree(x, z):

    trunk = Entity(
        model='cube',
        scale=(0.7, 3, 0.7),
        position=(x, 1.5, z),
        color=color.rgb(90, 50, 25),
        collider='box'
    )

    leaves = Entity(
        model='sphere',
        scale=2.5,
        position=(x, 3.5, z),
        color=color.rgb(30, 110, 40)
    )


create_tree(-10, 8)
create_tree(-7, 10)
create_tree(10, 10)
create_tree(11, -8)
create_tree(-10, -8)

# ==========================================
# بيت
# ==========================================

house = Entity(
    model='cube',
    scale=(8, 5, 7),
    position=(0, 2.5, 8),
    color=color.rgb(120, 80, 60),
    collider='box'
)

# باب البيت

door = Entity(
    model='cube',
    scale=(2, 3, 0.3),
    position=(0, 1.5, 4.45),
    color=color.rgb(60, 35, 20)
)

# نافذتين

window1 = Entity(
    model='cube',
    scale=(1.5, 1.5, 0.2),
    position=(-2.3, 3, 4.4),
    color=color.cyan
)

window2 = Entity(
    model='cube',
    scale=(1.5, 1.5, 0.2),
    position=(2.3, 3, 4.4),
    color=color.cyan
)

# ==========================================
# الشخصيات
# ==========================================

character_colors = [
    color.azure,
    color.orange,
    color.lime,
    color.violet
]

character_names = [
    "Blue",
    "Orange",
    "Green",
    "Purple"
]

selected_character = 0

# ==========================================
# إنشاء شخصية
# ==========================================

def create_character(position, character_color):

    character = Entity(
        position=position
    )

    # الجسم
    Entity(
        parent=character,
        model='cube',
        scale=(0.8, 1.4, 0.5),
        y=0.7,
        color=character_color
    )

    # الرأس
    Entity(
        parent=character,
        model='sphere',
        scale=0.7,
        y=1.7,
        color=color.rgb(240, 190, 150)
    )

    # العين اليمنى
    Entity(
        parent=character,
        model='sphere',
        scale=0.12,
        position=(0.18, 1.75, -0.32),
        color=color.black
    )

    # العين اليسرى
    Entity(
        parent=character,
        model='sphere',
        scale=0.12,
        position=(-0.18, 1.75, -0.32),
        color=color.black
    )

    # الرجل الأولى
    Entity(
        parent=character,
        model='cube',
        scale=(0.25, 0.8, 0.3),
        position=(-0.22, -0.1, 0),
        color=color.dark_gray
    )

    # الرجل الثانية
    Entity(
        parent=character,
        model='cube',
        scale=(0.25, 0.8, 0.3),
        position=(0.22, -0.1, 0),
        color=color.dark_gray
    )

    return character


# الشخصيات الموجودة في المكان

characters = []

characters.append(
    create_character((-5, 0, 0), color.azure)
)

characters.append(
    create_character((5, 0, 0), color.orange)
)

characters.append(
    create_character((0, 0, -5), color.lime)
)

characters.append(
    create_character((7, 0, -7), color.violet)
)

# ==========================================
# اللاعب
# ==========================================

player = characters[selected_character]

# إخفاء باقي الشخصيات مؤقتاً
for i in range(len(characters)):
    if i != selected_character:
        characters[i].enabled = False

# ==========================================
# إعداد الحركة
# ==========================================

player_speed = 5
run_speed = 9
jump_speed = 8

vertical_speed = 0
gravity = 20

# ==========================================
# الكاميرا
# ==========================================

camera.position = player.position + Vec3(0, 4, -8)

camera.fov = 70

# ==========================================
# واجهة
# ==========================================

title = Text(
    text="MY 3D ADVENTURE",
    origin=(0, 0),
    y=0.45,
    scale=1.5,
    color=color.azure
)

controls = Text(
    text="W A S D = حركة\nSHIFT = ركض\nSPACE = قفز\n1 2 3 4 = تغيير الشخصية",
    x=-0.85,
    y=0.38,
    scale=0.8,
    color=color.white
)

character_text = Text(
    text="الشخصية: Blue",
    x=-0.85,
    y=-0.35,
    scale=1,
    color=color.yellow
)

# ==========================================
# حركة اللاعب
# ==========================================

def update():

    global vertical_speed

    # --------------------------------------
    # السرعة
    # --------------------------------------

    speed = player_speed

    if held_keys['shift']:
        speed = run_speed

    # --------------------------------------
    # الاتجاه
    # --------------------------------------

    direction = Vec3(
        held_keys['d'] - held_keys['a'],
        0,
        held_keys['w'] - held_keys['s']
    )

    if direction.length() > 0:

        direction = direction.normalized()

        player.position += direction * speed * time.dt

        # الشخصية تنظر باتجاه الحركة
        player.look_at(
            player.position + direction,
            axis='y'
        )

    # --------------------------------------
    # الجاذبية
    # --------------------------------------

    vertical_speed -= gravity * time.dt

    player.y += vertical_speed * time.dt

    # --------------------------------------
    # الأرض
    # --------------------------------------

    if player.y < 0:

        player.y = 0
        vertical_speed = 0

    # --------------------------------------
    # القفز
    # --------------------------------------

    if held_keys['space'] and player.y <= 0.01:

        vertical_speed = jump_speed

    # --------------------------------------
    # الكاميرا
    # --------------------------------------

    target_camera = player.position + Vec3(0, 4, -8)

    camera.position = lerp(
        camera.position,
        target_camera,
        5 * time.dt
    )

    camera.look_at(
        player.position + Vec3(0, 1, 0)
    )

# ==========================================
# تغيير الشخصية
# ==========================================

def input(key):

    global selected_character
    global player

    if key in ['1', '2', '3', '4']:

        new_character = int(key) - 1

        if new_character < len(characters):

            # إخفاء القديمة
            for character in characters:
                character.enabled = False

            # اختيار الجديدة
            selected_character = new_character

            player = characters[selected_character]

            player.enabled = True

            player.position = (0, 0, 0)

            character_text.text = (
                "الشخصية: "
                + character_names[selected_character]
            )

            camera.position = player.position + Vec3(0, 4, -8)

# ==========================================
# تشغيل اللعبة
# ==========================================

app.run()
