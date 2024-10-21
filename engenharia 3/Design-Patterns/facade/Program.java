package facade;

import facade.baseClasses.DVDPlayer;
import facade.baseClasses.Lights;
import facade.baseClasses.Projector;
import facade.baseClasses.SoundSystem;
import facade.facades.HomeTheaterFacade;

public class Program {
    public static void main(String[] args) {

        DVDPlayer dvdPlayer = new DVDPlayer();
        Projector projector = new Projector();
        SoundSystem soundSystem = new SoundSystem();
        Lights lights = new Lights();

        HomeTheaterFacade homeTheater = new HomeTheaterFacade(dvdPlayer, projector, soundSystem, lights);

        homeTheater.watchMovie("Inception");

        System.out.println("\nAfter the movie...\n");

        homeTheater.endMovie();
    }
}
