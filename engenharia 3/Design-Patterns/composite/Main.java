package composite;

import composite.components.Directory;
import composite.components.File;
import composite.components.FileSystemComponent;

public class Main {
    public static void main(String[] args) {
        FileSystemComponent file1 = new File("file1.txt");
        FileSystemComponent file2 = new File("file2.txt");
        FileSystemComponent file3 = new File("file3.txt");

        Directory dir1 = new Directory("dir1");
        Directory dir2 = new Directory("dir2");

        dir1.add(file1);
        dir1.add(dir2);

        dir2.add(file2);
        dir2.add(file3);

        dir1.display("");
    }
}
