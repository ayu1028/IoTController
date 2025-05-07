document.addEventListener('DOMContentLoaded', function() {
    const all_btn_id_list = [
        'kaiteki',
        'teishi',
        'reibo',
        'danbo',
        'joshitsu',
        'kashitsu',
    ];

    const temp_id_list = [
        'reibo-temp',
        'danbo-temp',
        'kaiteki-temp'
    ];

    const hum_id_list = [
        'reibo-hum',
        'danbo-hum',
    ];

    const control_btn_id_list = [
        'kaiteki',
        'reibo',
        'danbo',
    ];

    const joshitsu_kashitsu_control_btn_list = [
        'joshitsu',
        'kashitsu',
    ];

    const reibo_temp_max = 32;
    const reibo_temp_min = 18;
    const reibo_hum_max = 60;
    const reibo_hum_min = 50;

    const danbo_temp_max = 30;
    const danbo_temp_min = 14;
    const danbo_hum_max = 50;
    const danbo_hum_min = 40;

    const kaiteki_temp_max = 8;
    const kaiteki_temp_min = -8;
    
    const teishi_btn = document.getElementById('teishi')
    const joshitsu_btn = document.getElementById('joshitsu')
    const kashitsu_btn = document.getElementById('kashitsu')

    const temp_btn = [...document.getElementsByClassName("temp")];
    const hum_btn = [...document.getElementsByClassName("hum")];

    const buttons = document.querySelectorAll('.tab-button');
    const contents = document.querySelectorAll('.tab-content');

    // 冷房、暖房、快適自動のボタンの挙動
    control_btn_id_list.forEach(idName => {
        const element = document.getElementById(idName);
        // 取得した HTMLCollection 内の各要素にイベントリスナーを追加
        element.addEventListener('click', function () {
            // すべての control_btn_class_list に対応する要素から 'active-btn' を削除
            all_btn_id_list.forEach(otherIdName => {
                const otherElement = document.getElementById(otherIdName);
                otherElement.classList.remove('active-btn');
            });

            temp_id_list.forEach(idName => {
                const element = document.getElementById(idName)
                if(!element.classList.contains('hidden')) {
                    element.classList.add('hidden');
                }
            });

            hum_id_list.forEach(idName => {
                const element = document.getElementById(idName)
                if(!element.classList.contains('hidden')) {
                    element.classList.add('hidden');
                }
            });
            // クリックされた要素に 'active-btn' を追加
            element.classList.add('active-btn');
            if(idName == 'reibo') {
                document.getElementById('reibo-temp').classList.remove('hidden');
                document.getElementById('state').textContent = '冷房';
            } else if (idName == 'danbo') {
                document.getElementById('danbo-temp').classList.remove('hidden');
                document.getElementById('state').textContent = '暖房';
            } else if (idName == 'kaiteki') {
                document.getElementById('kaiteki-temp').classList.remove('hidden');
                document.getElementById('state').textContent = '快適自動';
            }
        });
    });

    // 停止ボタンの挙動
    teishi_btn.addEventListener('click', function () {
        all_btn_id_list.forEach(idName => {
            const Element = document.getElementById(idName);
            Element.classList.remove('active-btn');
        });

        temp_id_list.forEach(idName => {
            const element = document.getElementById(idName)
            if(!element.classList.contains('hidden')) {
                element.classList.add('hidden');
            }
        });

        hum_id_list.forEach(idName => {
            element = document.getElementById(idName);
            if(!element.classList.contains('hidden')) {
                element.classList.add('hidden');
            }
        });
        this.classList.add('active-btn');
        document.getElementById('state').textContent = '停止';
    });

    // 除湿ボタンの挙動
    joshitsu_btn.addEventListener('click', function () {
        const reibo_btn = document.getElementById('reibo');

        if(reibo_btn.classList.contains('active-btn')) {
            joshitsu_kashitsu_control_btn_list.forEach(idName => {
                const element = document.getElementById(idName);
                element.classList.remove('active-btn');
            });
            hum_id_list.forEach(idName => {
                element = document.getElementById(idName);
                if(!element.classList.contains('hidden')) {
                    element.classList.add('hidden');
                }
            });
            this.classList.add('active-btn');
            document.getElementById('reibo-hum').classList.remove('hidden');
            document.getElementById('state').textContent = '除湿冷房';
        }
    });

    // 加湿ボタンの挙動
    kashitsu_btn.addEventListener('click', function () {
        const danbo_btn = document.getElementById('danbo');

        if(danbo_btn.classList.contains('active-btn')) {
            joshitsu_kashitsu_control_btn_list.forEach(idName => {
                const element = document.getElementById(idName);
                element.classList.remove('active-btn');
            });
            hum_id_list.forEach(idName => {
                element = document.getElementById(idName);
                if(!element.classList.contains('hidden')) {
                    element.classList.add('hidden');
                }
            });
            this.classList.add('active-btn');
            document.getElementById('danbo-hum').classList.remove('hidden');
            document.getElementById('state').textContent = '加湿暖房';
        }
    });

    // 温度調整(up/down)ボタンの挙動
    temp_btn.forEach(btn => {
        btn.addEventListener('click', function() {
            const btn_text = this.textContent;
            const reibo_temp_before = Number(document.getElementById("reibo-temp").textContent);
            const danbo_temp_before = Number(document.getElementById("danbo-temp").textContent);
            const kaiteki_temp_before = Number(document.getElementById("kaiteki-temp").textContent);
            
            if(btn_text == "up") {
                if(document.getElementById('reibo').classList.contains('active-btn')) {
                    temp = reibo_temp_before + 0.5;
                    if(temp >= reibo_temp_max) {
                        temp = reibo_temp_max;
                    }
                    document.getElementById("reibo-temp").textContent = temp;
                } else if(document.getElementById('danbo').classList.contains('active-btn')) {
                    temp = danbo_temp_before + 0.5;
                    if(temp >= danbo_temp_max) {
                        temp = danbo_temp_max;
                    }
                    document.getElementById("danbo-temp").textContent = temp;
                } else if(document.getElementById('kaiteki').classList.contains('active-btn')) {
                    temp = kaiteki_temp_before + 0.5;
                    if(temp >= kaiteki_temp_max) {
                        temp = kaiteki_temp_max;
                    }
                    document.getElementById("kaiteki-temp").textContent = temp;
                }

            } else if(btn_text == "down") {
                if(document.getElementById('reibo').classList.contains('active-btn')) {
                    temp = reibo_temp_before - 0.5;
                    if(temp <= reibo_temp_min) {
                        temp = reibo_temp_min;
                    }
                    document.getElementById("reibo-temp").textContent = temp;
                } else if(document.getElementById('danbo').classList.contains('active-btn')) {
                    temp = danbo_temp_before - 0.5;
                    if(temp <= danbo_temp_min) {
                        temp = danbo_temp_min;
                    }
                    document.getElementById("danbo-temp").textContent = temp;
                } else if(document.getElementById('kaiteki').classList.contains('active-btn')) {
                    temp = kaiteki_temp_before - 0.5;
                    if(temp <= kaiteki_temp_min) {
                        temp = kaiteki_temp_min;
                    }
                    document.getElementById("kaiteki-temp").textContent = temp;
                }
            }
        });
    });

    // 湿度調整(up/down)ボタンの挙動
    hum_btn.forEach(btn => {
        btn.addEventListener('click', function() {
            const btn_text = this.textContent;
            const reibo_hum_before = Number(document.getElementById("reibo-hum").textContent);
            const danbo_hum_before = Number(document.getElementById("danbo-hum").textContent);
            
            if(btn_text == "up") {
                if(document.getElementById('reibo').classList.contains('active-btn')) {
                    hum = reibo_hum_before + 5;
                    if(hum >= reibo_hum_max) {
                        hum = reibo_hum_max;
                    }
                    document.getElementById("reibo-hum").textContent = hum;
                } else if(document.getElementById('danbo').classList.contains('active-btn')) {
                    hum = danbo_hum_before + 5;
                    if(hum >= danbo_hum_max) {
                        hum = danbo_hum_max;
                    }
                    document.getElementById("danbo-hum").textContent = hum;
                }

            } else if(btn_text == "down") {
                if(document.getElementById('reibo').classList.contains('active-btn')) {
                    hum = reibo_hum_before - 5;
                    if(hum <= reibo_hum_min) {
                        hum = reibo_hum_min;
                    }
                    document.getElementById("reibo-hum").textContent = hum;
                } else if(document.getElementById('danbo').classList.contains('active-btn')) {
                    hum = danbo_hum_before - 5;
                    if(hum <= danbo_hum_min) {
                        hum = danbo_hum_min;
                    }
                    document.getElementById("danbo-hum").textContent = hum;
                }
            }
        });
    });

    // fetch用AddEventListener

    // タブボタンの挙動
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

    temp_id_list.forEach(idName => {
        document.getElementById(idName).classList.add('hidden');
    });

    hum_id_list.forEach(idName => {
        document.getElementById(idName).classList.add('hidden');
    });

});
