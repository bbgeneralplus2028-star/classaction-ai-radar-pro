export async function requestNotificationPermission() {

  if ("Notification" in window) {
    await Notification.requestPermission();
  }

}

export function showPopup(title, body) {

  if (Notification.permission === "granted") {

    new Notification(title, {
      body: body
    });

  }

}
