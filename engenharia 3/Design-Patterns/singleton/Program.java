package singleton;

public class Program {
    public static void main(String[] args) {
        ConfigurationManager config = ConfigurationManager.getInstance();

        System.out.println("Database URL: " + config.getDatabaseUrl());
        System.out.println("API Key: " + config.getApiKey());

        config.setDatabaseUrl("jdbc:mysql://localhost:3306/otherdb");
        config.setApiKey("XYZ789");

        ConfigurationManager anotherConfig = ConfigurationManager.getInstance();

        System.out.println("\nAfter modifications:");
        System.out.println("Database URL: " + anotherConfig.getDatabaseUrl());
        System.out.println("API Key: " + anotherConfig.getApiKey());
    }
}
