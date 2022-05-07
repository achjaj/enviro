package com.achjaj.enviz;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.TreeItem;
import javafx.scene.control.TreeView;

import java.io.File;
import java.net.URL;
import java.util.ResourceBundle;

public class Window implements Initializable {
    @FXML
    TreeView<String> dsView;

    private TreeItem<String> datasets;

    private TreeItem<String> crawlLocal(File file) {
        var root = new TreeItem<>(file.getName());

        var files = file.listFiles();
        if (files != null) {
            for (var child : files) {
                var childItem = child.isDirectory() ? crawlLocal(child) :
                    new TreeItem<>(child.getName());

                root.getChildren().add(childItem);
            }
        }

        return root;
    }

    @FXML
    void addLocalAction() {
        Dialogs.openDir().ifPresent(file -> datasets.getChildren().add(crawlLocal(file)));
    }

    @FXML
    void remove() {
        var label = dsView.getSelectionModel().getSelectedItem().getValue();
        datasets.getChildren().stream().filter(child -> child.getValue().equals(label))
            .findAny()
            .ifPresent(child -> datasets.getChildren().remove(child));
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        datasets = new TreeItem<>("Datasets");
        datasets.setExpanded(true);
        dsView.setRoot(datasets);
    }
}
