document.addEventListener('DOMContentLoaded', function() {
    const all_btn_id_list = [
        'kaiteki',
        'teishi',
        'reibo',
        'danbo',
        'joshitsu',
        'kashitsu',
    ];

    const control_btn_id_list = [
        'kaiteki',
        // 'teishi',
        'reibo',
        'danbo',
        // 'joshitsu',
        // 'kashitsu',
    ];

    const joshitsu_kashitsu_control_btn_list = [
        'joshitsu',
        'kashitsu',
    ];

    const teishi_btn = document.getElementById('teishi')
    const joshitsu_btn = document.getElementById('joshitsu')
    const kashitsu_btn = document.getElementById('kashitsu')

    const temp_btn = [...document.getElementsByClassName("temp")];
    const hum_btn = [...document.getElementsByClassName("hum")];

    const buttons = document.querySelectorAll('.tab-button');
    const contents = document.querySelectorAll('.tab-content');
    const targetDiv = document.getElementById('tab3');

    control_btn_id_list.forEach(idName => {
        const element = document.getElementById(idName);
        // 取得した HTMLCollection 内の各要素にイベントリスナーを追加
        element.addEventListener('click', function () {
            // すべての control_btn_class_list に対応する要素から 'active-btn' を削除
            all_btn_id_list.forEach(otherIdName => {
                const otherElement = document.getElementById(otherIdName);
                otherElement.classList.remove('active-btn');
            });
            // クリックされた要素に 'active-btn' を追加
            element.classList.add('active-btn');
        });
    });

    teishi_btn.addEventListener('click', function () {
        all_btn_id_list.forEach(idName => {
            const Element = document.getElementById(idName);
            Element.classList.remove('active-btn');
        });
        this.classList.add('active-btn');
    });

    joshitsu_btn.addEventListener('click', function () {
        if(document.getElementById('reibo').classList.contains('active-btn')) {
            joshitsu_kashitsu_control_btn_list.forEach(idName => {
                const element = document.getElementById(idName);
                element.classList.remove('active-btn');
            });
            this.classList.add('active-btn');
        }
    });

    kashitsu_btn.addEventListener('click', function () {
        if(document.getElementById('danbo').classList.contains('active-btn')) {
            joshitsu_kashitsu_control_btn_list.forEach(idName => {
                const element = document.getElementById(idName);
                element.classList.remove('active-btn');
            });
            this.classList.add('active-btn');
        }
    });

    temp_btn.forEach(btn => {
        btn.addEventListener('click', function() {
            const btn_text = this.textContent
            const ondo_before = Number(document.getElementById("ondo-settei").textContent)
            if(btn_text == "up") {
                document.getElementById("ondo-settei").textContent = ondo_before + 0.5
            } else if(btn_text == "down") {
                document.getElementById("ondo-settei").textContent = ondo_before - 0.5
            }
        });
    });

    hum_btn.forEach(btn => {
        btn.addEventListener('click', function() {
            const btn_text = this.textContent
            const hum_before = Number(document.getElementById("shitsudo-settei").textContent)
            if(btn_text == "up") {
                document.getElementById("shitsudo-settei").textContent = hum_before + 5
            } else if(btn_text == "down") {
                document.getElementById("shitsudo-settei").textContent = hum_before - 5
            }
        });
    });

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');

            contents.forEach(content => {
                content.classList.remove('active');
            });

            document.getElementById(tabId).classList.add('active');
        });
    });

    // 初期表示
    document.getElementById('tab1').classList.add('active');

});
