package strategy;

import strategy.frete.Frete;

import java.time.LocalDate;

public class Venda {
    private int codigo;
    private LocalDate dataDaVenda;
    private LocalDate dateDeEntrega;
    private Produto produto;
    private Frete frete;

    public Venda(int codigo, LocalDate dataDaVenda, LocalDate dateDeEntrega, Produto produtos, Frete frete) {
        this.codigo = codigo;
        this.dataDaVenda = dataDaVenda;
        this.dateDeEntrega = dateDeEntrega;
        this.produto = produtos;
        this.frete = frete;
    }

    public int getCodigo() {
        return codigo;
    }

    public void setCodigo(int codigo) {
        this.codigo = codigo;
    }

    public LocalDate getDataDaVenda() {
        return dataDaVenda;
    }

    public void setDataDaVenda(LocalDate dataDaVenda) {
        this.dataDaVenda = dataDaVenda;
    }

    public Produto getProdutos() {
        return produto;
    }

    public void setProduto(Produto produto) {
        this.produto = produto;
    }

    public Frete getFrete() {
        return frete;
    }

    public void setFrete(Frete frete) {
        this.frete = frete;
    }

    public LocalDate getDateDeEntrega() {
        return dateDeEntrega;
    }

    public void setDateDeEntrega(LocalDate dateDeEntrega) {
        this.dateDeEntrega = dateDeEntrega;
    }
}
