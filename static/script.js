document.addEventListener('DOMContentLoaded', function() {
    const control_btn_class_list = [
        'kaiteki',
        'teishi',
        'reibo',
        'danbo',
        'joshitsu',
        'kashitsu',
    ];
    const buttons = document.querySelectorAll('.tab-button');
    const contents = document.querySelectorAll('.tab-content');
    const temp_btn = [...document.getElementsByClassName("temp")];
    const hum_btn = [...document.getElementsByClassName("hum")];
    const targetDiv = document.getElementById('tab3');

    let control_btn = [];

    control_btn_class_list.forEach(className => {
        const elements = document.getElementsByClassName(className);
        // 取得した HTMLCollection 内の各要素にイベントリスナーを追加
        Array.from(elements).forEach(element => {
            element.addEventListener('click', function () {
                // すべての control_btn_class_list に対応する要素から 'active-btn' を削除
                control_btn_class_list.forEach(otherClassName => {
                    const otherElements = document.getElementsByClassName(otherClassName);
                    Array.from(otherElements).forEach(otherElement => {
                        otherElement.classList.remove('active-btn');
                    });
                });
                // クリックされた要素に 'active-btn' を追加
                this.classList.add('active-btn');
            });
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

    // 初期表示
    document.getElementById('tab1').classList.add('active');

});
