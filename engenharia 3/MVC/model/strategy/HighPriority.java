package model.strategy;

public class HighPriority implements PriorityStrategy {
    @Override
    public String getPriority() {
        return "Alta";
    }
}
