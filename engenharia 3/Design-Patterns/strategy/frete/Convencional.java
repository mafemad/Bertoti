package strategy.frete;

import strategy.Produto;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;

public class Convencional implements Frete{

    @Override
    public double cacular(Produto p, LocalDate d) {
        BigDecimal bd = BigDecimal.valueOf(p.getPeso() * 0.25).setScale(2, RoundingMode.HALF_UP);
        return  bd.doubleValue();
    }
}
