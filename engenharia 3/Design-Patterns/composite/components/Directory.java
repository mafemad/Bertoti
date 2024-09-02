package composite.components;

import java.util.ArrayList;
import java.util.List;

public class Directory implements FileSystemComponent {
    private String name;
    private List<FileSystemComponent> components = new ArrayList<>();

    public Directory(String name) {
        this.name = name;
    }

    @Override
    public void display(String indent) {
        System.out.println(indent + "Directory: " + name);
        for (FileSystemComponent component : components) {
            component.display(indent + "    ");
        }
    }

    public void add(FileSystemComponent component) {
        components.add(component);
    }

    public void remove(FileSystemComponent component) {
        components.remove(component);
    }
}
