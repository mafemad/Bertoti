import controller.TaskController;
import model.*;
import model.strategy.HighPriority;
import model.strategy.LowPriority;
import model.strategy.MediumPriority;
import model.strategy.PriorityStrategy;
import view.ConsoleView;

import java.util.Scanner;

public class App {
    public static void main(String[] args) {
        ConsoleView view = new ConsoleView();
        TaskController controller = new TaskController(view);
        Scanner scanner = new Scanner(System.in);

        // Exemplo inicial
        Task task1 = new SimpleTask("Comprar Material", new HighPriority());
        Task task2 = new SimpleTask("Enviar Relatório", new MediumPriority());

        CompositeTask project = new CompositeTask("Projeto Desenvolvimento", new HighPriority());
        project.addSubtask(new SimpleTask("Design do Produto", new MediumPriority()));
        project.addSubtask(new SimpleTask("Implementação do Código", new HighPriority()));

        controller.addTask(task1);
        controller.addTask(task2);
        controller.addTask(project);

        controller.displayTasks();

        // Menu interativo
        boolean running = true;
        while (running) {
            System.out.println("\nEscolha uma operação:");
            System.out.println("1 - Listar todas as tarefas");
            System.out.println("2 - Adicionar nova tarefa simples");
            System.out.println("3 - Adicionar nova tarefa composta");
            System.out.println("4 - Atualizar status de uma tarefa");
            System.out.println("5 - Sair");

            int choice = scanner.nextInt();
            scanner.nextLine(); // Limpar o buffer

            switch (choice) {
                case 1:
                    controller.displayTasks();
                    break;

                case 2:
                    System.out.print("Nome da tarefa: ");
                    String simpleTaskName = scanner.nextLine();
                    System.out.print("Prioridade (alta, média, baixa): ");
                    String simplePriority = scanner.nextLine();

                    PriorityStrategy priority = getPriorityStrategy(simplePriority);
                    Task simpleTask = new SimpleTask(simpleTaskName, priority);
                    controller.addTask(simpleTask);
                    System.out.println("Tarefa simples adicionada.");
                    break;

                case 3:
                    System.out.print("Nome da tarefa composta: ");
                    String compositeTaskName = scanner.nextLine();
                    System.out.print("Prioridade (alta, média, baixa): ");
                    String compositePriority = scanner.nextLine();

                    PriorityStrategy compositePriorityStrategy = getPriorityStrategy(compositePriority);
                    CompositeTask compositeTask = new CompositeTask(compositeTaskName, compositePriorityStrategy);

                    System.out.print("Quantas subtarefas?: ");
                    int subtaskCount = scanner.nextInt();
                    scanner.nextLine();

                    for (int i = 0; i < subtaskCount; i++) {
                        System.out.print("Nome da subtarefa " + (i + 1) + ": ");
                        String subtaskName = scanner.nextLine();
                        System.out.print("Prioridade da subtarefa (alta, média, baixa): ");
                        String subtaskPriority = scanner.nextLine();
                        PriorityStrategy subtaskPriorityStrategy = getPriorityStrategy(subtaskPriority);

                        Task subtask = new SimpleTask(subtaskName, subtaskPriorityStrategy);
                        compositeTask.addSubtask(subtask);
                    }

                    controller.addTask(compositeTask);
                    System.out.println("Tarefa composta adicionada.");
                    break;

                case 4:
                    System.out.print("Nome da tarefa para atualizar: ");
                    String taskName = scanner.nextLine();
                    Task taskToUpdate = findTaskByName(controller, taskName);

                    if (taskToUpdate != null) {
                        System.out.print("Novo status: ");
                        String newStatus = scanner.nextLine();
                        controller.updateTaskStatus(taskToUpdate, newStatus);
                        System.out.println("Status atualizado.");
                    } else {
                        System.out.println("Tarefa não encontrada.");
                    }
                    break;

                case 5:
                    running = false;
                    System.out.println("Saindo...");
                    break;

                default:
                    System.out.println("Escolha inválida.");
                    break;
            }
        }

        scanner.close();
    }

    private static PriorityStrategy getPriorityStrategy(String priority) {
        switch (priority.toLowerCase()) {
            case "alta":
                return new HighPriority();
            case "média":
                return new MediumPriority();
            case "baixa":
                return new LowPriority();
            default:
                System.out.println("Prioridade inválida, usando 'baixa' por padrão.");
                return new LowPriority();
        }
    }

    private static Task findTaskByName(TaskController controller, String taskName) {
        for (Task task : controller.getTasks()) {
            if (task.getName().equalsIgnoreCase(taskName)) {
                return task;
            }
        }
        return null;
    }
}
