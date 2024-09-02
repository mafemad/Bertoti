package observer.observers;

public class PurchaseDepartment implements Observer {
    @Override
    public void update(String product, int quantity) {
        if (quantity < 10) {
            System.out.println("Purchase Department: Time to reorder " + product + "!");
        }
    }
}