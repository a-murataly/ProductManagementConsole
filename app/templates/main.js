async function upload() {
    const fileInput = document.getElementById("fileInput"); //здесь я беру в руки файлик, который ввел юзер
    const file = fileInput.files[0];                        //здесь я беру первый имеющийся файл из массива
    if (!file) return alert("Сначала выберите файл");       //проверяю есть ли файл

    const formData = new FormData();                        //готовлю форму отправки на сервер
    formData.append("file", file);                          //добавляю в форму файл

    const selectedBrand = document.getElementById("brandSelect").value; //беру в руки название бренда, который юзер выбрал в селекторе
    formData.append("brand",selectedBrand);                 //добавляю название бренда в форму отправки
                                                            //форма уже содержит файл и название бренда

    const response = await fetch("/upload_csv", {           //отправляю заполненную форму на сервер, сразу беру в руки ответ
    method: "POST",
    body: formData
    });

    const data = await response.json();                     //превращаем ответ в объект

    if (!response.ok || !data.filtered_factors) {           //работаем с возможными ошибками
    document.getElementById("result").innerText =
        "Ошибка: " + (data.error ?? "Нет данных от сервера");
    return;                                                 //звершаем всю программу если ошибка
    }

    // Показываем данные в виде списка
    const html = data["filtered_factors"].map(row => `      
    <div>От: <b>${row.from}</b> → <b>${row.to}</b>, коэффициент: <b>${row.scaling_factor}</b></div>
    `).join("");                                            //создаем html-код из элементов объекта ответа и соединяем их вместе
    document.getElementById("result").innerHTML = html;     //в id ответа в html вставляем собранный html-код

    // Селектор брендов
    const brands = data.filters["Brand"];                   //берем из ответа upload_csv всё поле брендов как массив
    const select = document.getElementById("brandSelect");  //создаем селектор который будет тянуть из id
    select.innerHTML = "";                                  //инициализируем его пустым

    brands.forEach(brand => {                               //проходим по каждому элементу массива чтобы...
    const option = document.createElement("option");        //...создать опции из брендов
    option.value = brand;
    option.text = brand;
    select.appendChild(option);                             //добавляем к селектору
    });

    // Обработчик на смену бренда
    select.addEventListener("change", () => {               
    const selectedBrand = select.value;
    drawChart(data, selectedBrand);
    });

    // Построение графика по первому бренду
    drawChart(data, brands[0]);
}

function drawChart(data, selectedBrand) {
    const chart = echarts.init(document.getElementById("chart"));

    const fltrd_Brand = data.filtered_factors.filter(r => r.Brand === selectedBrand);
    const labels = fltrd_Brand.map(r => `${r.from} → ${r.to}`);
    const filteredData_filtered = fltrd_Brand.map(r => r.scaling_factor);
    const baselineData = data.baseline_factors.map(r => r.scaling_factor);

    console.log("Selected brand:", selectedBrand);
    console.log("Filtered rows:", fltrd_Brand);
    console.log("Filtered values:", filteredData_filtered);
    console.log("Пример строки:", data.filtered_factors[0]);


    chart.setOption({
    title: { text: "Сравнение с категорией" },
    tooltip: { trigger: 'axis' },
    legend: { data: ['Filtered', 'Baseline'] },
    xAxis: {
        type: 'category',
        data: labels,
        axisLabel: { rotate: 45 }
    },
    yAxis: { type: 'value' },
    series: [
        {
        name: 'Filtered',
        type: 'bar',
        data: filteredData_filtered,
        barGap: 0
        },
        {
        name: 'Baseline',
        type: 'bar',
        data: baselineData
        }
    ]
    });
}