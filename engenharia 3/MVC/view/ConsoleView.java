package view;

import model.Task;
import model.observer.TaskObserver;

public class ConsoleView implements TaskObserver {
    @Override
    public void update(String taskName, String status) {
        System.out.println("Notificação: Tarefa \"" + taskName + "\" foi atualizada para o status: " + status);
    }

    public void showTask(Task task) {
        task.showTaskDetails();
    }
}
