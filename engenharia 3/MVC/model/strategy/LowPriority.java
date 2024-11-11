package model.strategy;

public class LowPriority implements PriorityStrategy {
    @Override
    public String getPriority() {
        return "Baixa";
    }
}
