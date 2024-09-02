package observer;

import observer.observers.PurchaseDepartment;
import observer.observers.ReportSystem;
import observer.observers.SalesDepartment;

public class Main {
    public static void main(String[] args) {
        Stock stock = new Stock("Laptop", 20);

        PurchaseDepartment purchase = new PurchaseDepartment();
        SalesDepartment sales = new SalesDepartment();
        ReportSystem report = new ReportSystem();

        stock.addObserver(purchase);
        stock.addObserver(sales);
        stock.addObserver(report);

        // Change the stock and observe the notifications
        stock.setQuantity(15);  // Relatório do sistema é notificado
        stock.setQuantity(5);   // Departamento de compras é notificado
        stock.setQuantity(0);   // Departamento de vendas e compras são notificados
    }
}

