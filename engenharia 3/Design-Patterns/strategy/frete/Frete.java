package strategy.frete;

import strategy.Produto;

import java.time.LocalDate;

public interface Frete {

    double cacular(Produto p, LocalDate d);
}
