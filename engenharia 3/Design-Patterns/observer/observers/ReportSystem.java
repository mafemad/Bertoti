package observer.observers;

public class ReportSystem implements Observer {
    @Override
    public void update(String product, int quantity) {
        System.out.println("Report System: " + product + " quantity changed to " + quantity);
    }
}