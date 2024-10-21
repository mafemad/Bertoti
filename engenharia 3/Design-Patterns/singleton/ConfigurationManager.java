package singleton;

public class ConfigurationManager {

    private static ConfigurationManager instance;

    private String databaseUrl;
    private String apiKey;

    private ConfigurationManager() {
        this.databaseUrl = "jdbc:mysql://localhost:3306/mydb";
        this.apiKey = "ABC123";
    }

    public static ConfigurationManager getInstance() {
        if (instance == null) {
            instance = new ConfigurationManager();
        }
        return instance;
    }

    public String getDatabaseUrl() {
        return databaseUrl;
    }

    public void setDatabaseUrl(String databaseUrl) {
        this.databaseUrl = databaseUrl;
    }

    public String getApiKey() {
        return apiKey;
    }

    public void setApiKey(String apiKey) {
        this.apiKey = apiKey;
    }
}

