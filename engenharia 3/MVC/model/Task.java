package model;

import model.observer.TaskObserver;
import model.strategy.PriorityStrategy;

import java.util.ArrayList;
import java.util.List;

public abstract class Task {
    protected String name;
    protected String status;
    protected PriorityStrategy priority;
    protected List<TaskObserver> observers = new ArrayList<>();

    public Task(String name, PriorityStrategy priority) {
        this.name = name;
        this.priority = priority;
        this.status = "Pendente";
    }

    public String getName() {
        return name;
    }

    public void setStatus(String status) {
        this.status = status;
        notifyObservers();
    }

    public String getStatus() {
        return status;
    }

    public String getPriority() {
        return priority.getPriority();
    }

    public void addObserver(TaskObserver observer) {
        observers.add(observer);
    }

    public void notifyObservers() {
        for (TaskObserver observer : observers) {
            observer.update(name, status);
        }
    }

    public abstract void showTaskDetails();
}
