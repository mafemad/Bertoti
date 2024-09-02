package observer;

import observer.observers.Observer;

import java.util.ArrayList;
import java.util.List;

public class Stock {
    private List<Observer> observers = new ArrayList<>();
    private String product;
    private int quantity;

    public Stock(String product, int quantity) {
        this.product = product;
        this.quantity = quantity;
    }

    public void addObserver(Observer observer) {
        observers.add(observer);
    }

    public void removeObserver(Observer observer) {
        observers.remove(observer);
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
        notifyAllObservers();
    }

    private void notifyAllObservers() {
        for (Observer observer : observers) {
            observer.update(product, quantity);
        }
    }
}
