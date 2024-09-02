package strategy;

import strategy.frete.Agendado;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class Main {
    public static void main(String[] args) {

        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("dd/MM/yyyy");

        Produto p1 = new Produto("cadeira ergonomica", 2000.0,3.328);
        Produto p2 = new Produto("mesa ajustavel", 3000.0,5.345);

        Venda venda = new Venda(1,LocalDate.now(), LocalDate.parse("26/08/2024", fmt), p1, new Agendado());

        System.out.println(venda.getFrete().cacular(venda.getProdutos(), venda.getDateDeEntrega()));
    }
}
