start();
 
function start() {
    auto.waitFor();
    console.show();
    console.setPosition(0, 0);
    CustomSleep(1, 2, "【日志窗】启动中…");
    console.setSize(device.width, device.height / 3);

    CustomSleep(0.1, 0.5, "请授权截图！");
    if (requestScreenCapture()) CustomSleep(1, 2, "即将启动【手机京东】…");
    else {
        CustomSleep(0.1, 0.5, "【截图授权】失败！");
        CustomExit();
    }

    app.launch("com.jingdong.app.mall");
    CustomSleep(3, 5, "【手机京东】启动中…");

    while (textMatches(/累计任务奖励/) == null) CustomSleep(3, 5, "请手动进入活动页面，并打开任务列表…");
    //开始任务
    doTask();
}
function doTask() {

    CustomSleep(0.1, 0.5, "【11.11】发现任务列表");

    while (true) {
        let taskButtons = null;
        for (let index = 0; index < 3; index++) {
            taskButtons = GetTaskLogo();
            if (taskButtons == null || taskButtons.empty()) {
                if (textMatches(/累计任务奖励/) == null) CustomBack();
                else continue;
            }
            else break;
        }

        if (taskButtons == null || taskButtons.empty()) {
            CustomSleep(0.1, 0.5, "【浏览任务】未找到…");
            CustomExit();
        }
        else CustomSleep(0.1, 0.5, "共找到【" + taskButtons.length + "】个任务。");

        let taskButton, taskText
        let img = captureScreen();
        for (let i = 0; i < taskButtons.length; i++) {
            let item = taskButtons[i];
            taskText = item.text();
            item = item.parent().child(3);
            let b = item.bounds();
            let color = images.pixel(img, b.left + b.width() / 10, b.top + b.height() / 2);
            if (colors.isSimilar(color, '#fe2a60')) {
                taskButton = item;
                break;
            }
            else CustomSleep(0.1, 0.5, "【" + i + 1 + "、" + taskText + "】已完成。");
        }

        if (!taskButton) {
            CustomSleep(0.1, 0.5, "【未完成任务】未找到…");
            CustomExit();
        }

        if (taskText.match(/浏览并关注|浏览可得/)) {
            CustomSleep(0.1, 0.5, "即将进行【" + taskText + "】");
            taskButton.click();
            CustomSleep(1, 3, "【" + taskText + "】进行中…");
            CustomSleep(8, 12, "【浏览】浏览中", true);
        } else if (taskText.match(/累计浏览/)) {
            CustomSleep(0.1, 0.5, "即将进行【" + taskText + "】");
            taskButton.click();
            CustomSleep(5, 10, "【" + taskText + "】进行中…");
            if (taskText.match(/加购/)) itemTask(true);
            else itemTask(false);
        } else if (taskText.match(/成功入会/)) {
            CustomSleep(0.1, 0.5, "即将进行【" + taskText + "】");
            taskButton.click();
            CustomSleep(1, 3, "【" + taskText + "】进行中…");
            if (textContains("加入店铺会员").exists()) { CustomSleep(0.1, 0.5, "脚本结束（涉及个人隐私，请手动加入店铺会员或者忽略加入会员任务）"); break; }
        } else if (taskText.match(/浏览.*s/)) {
            CustomSleep(0.1, 0.5, "即将进行【" + taskText + "】");
            taskButton.click();
            CustomSleep(3, 5, "【" + taskText + "】进行中…");
            CustomSleep(8, 12, "【浏览】浏览中", true);
        }
        else {
            CustomSleep(0.1, 0.5, "无效任务【" + taskText + "】");
            CustomSleep(0.1, 0.5, "任务结束（如有尚未完成的任务，请手动完成或重新执行）"); break;
        }

        CustomBack();
    }
    alert('任务完成！')
}

function itemTask(cart) {
    var items = textContains('.jpg!q70').find();
    var maxCount = items.length;
    var addCount = parseInt(Math.ceil(random(5, 7)), 10);
    var addedCount = 1;
    for (var i = 0; i < maxCount && addedCount <= addCount; i++) {
        if (i > 0 && i % 4 == 0) className("android.view.View").scrollForward();
        var index = parseInt(Math.ceil(random(1, 3)), 10);
        CustomSleep(0.1, 0.5, "掷骰中：" + index);
        if (index % 2 == 1) {
            if (cart) {
                CustomSleep(0.1, 0.5, '加购并浏览')
                items[i].parent().parent().child(5).click();
            } else {
                CustomSleep(0.1, 0.5, '浏览商品页')
                items[i].parent().parent().child(4).click();
            }
            CustomSleep(3, 6, "【" + addedCount + "/" + addCount + "】浏览中", true);
            CustomBack();
            addedCount++;
        }
    }
}

function GetTaskLogo() {
    CustomSleep(0.1, 0.5, "即将【寻找任务】");
    return textMatches(/.*浏览并关注.*|.*成功入会.*|.*浏览[0-9]s.*|.*累计浏览.*|.*浏览可得.*/).find();
}

function CustomSleep(minNum, maxNum, msg, scroll) {
    console.info(msg);
    if (maxNum > 0 && maxNum > minNum) {
        var sleeptimes = parseInt(random(minNum * 1000, maxNum * 1000), 10);
        var tick = 1000;
        for (var i = 0; i < sleeptimes; i += tick) {
            var strlog = "";
            for (var j = 0; j < parseInt(Math.ceil((sleeptimes - i) / tick), 10); j++) { strlog += "."; }
            console.verbose(strlog);
            sleep(tick);
            if (scroll) scrollDown();
        }
    }
}
 
function CustomBack() {
    back();
    CustomSleep(2, 4, "返回中");
}
 
function CustomExit() {
    CustomSleep(2, 4, "脚本即将终止运行");
    exit();
}