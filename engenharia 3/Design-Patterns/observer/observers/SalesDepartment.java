package observer.observers;

public class SalesDepartment implements Observer {
    @Override
    public void update(String product, int quantity) {
        if (quantity == 0) {
            System.out.println("Sales Department: " + product + " is out of stock. Stop selling it!");
        }
    }
}