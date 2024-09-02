package strategy.frete;

import strategy.Produto;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public class Agendado implements Frete{
    @Override
    public double cacular(Produto p, LocalDate d) {
        LocalDate now = LocalDate.now();
        long diferenca = ChronoUnit.WEEKS.between(now, d);
        BigDecimal bd = BigDecimal.valueOf(p.getPeso() * 0.40 + diferenca * 2).setScale(2, RoundingMode.HALF_UP);
        return  bd.doubleValue();
    }
}
