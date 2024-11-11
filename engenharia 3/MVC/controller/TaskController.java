// controller/TaskController.java
package controller;

import model.Task;
import view.ConsoleView;
import java.util.ArrayList;
import java.util.List;

public class TaskController {
    private List<Task> tasks = new ArrayList<>();
    private ConsoleView view;

    public TaskController(ConsoleView view) {
        this.view = view;
    }

    public void addTask(Task task) {
        tasks.add(task);
        task.addObserver(view);  // Adiciona a view como observadora da tarefa
    }

    public void updateTaskStatus(Task task, String status) {
        task.setStatus(status);
    }

    public void displayTasks() {
        for (Task task : tasks) {
            view.showTask(task);
        }
    }

    public List<Task> getTasks() {
        return tasks;
    }
}
