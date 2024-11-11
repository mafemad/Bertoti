package model;

import model.strategy.PriorityStrategy;

public class SimpleTask extends Task {
    public SimpleTask(String name, PriorityStrategy priority) {
        super(name, priority);
    }

    @Override
    public void showTaskDetails() {
        System.out.println("Tarefa: " + name + ", Prioridade: " + getPriority() + ", Status: " + status);
    }
}
