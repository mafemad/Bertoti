package model;

import model.strategy.PriorityStrategy;

import java.util.ArrayList;
import java.util.List;

public class CompositeTask extends Task {
    private List<Task> subtasks = new ArrayList<>();

    public CompositeTask(String name, PriorityStrategy priority) {
        super(name, priority);
    }

    public void addSubtask(Task task) {
        subtasks.add(task);
    }

    @Override
    public void showTaskDetails() {
        System.out.println("Tarefa Composta: " + name + ", Prioridade: " + getPriority() + ", Status: " + status);
        for (Task subtask : subtasks) {
            subtask.showTaskDetails();
        }
    }
}
