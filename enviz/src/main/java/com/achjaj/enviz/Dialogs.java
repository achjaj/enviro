package com.achjaj.enviz;

import javafx.stage.DirectoryChooser;
import javafx.stage.FileChooser;

import java.io.File;
import java.util.Optional;

public class Dialogs {
    static Optional<File> openFile() {
        var chooser = new FileChooser();
        return Optional.ofNullable(chooser.showOpenDialog(null));
    }

    static Optional<File> openDir() {
        var chooser = new DirectoryChooser();
        return Optional.ofNullable(chooser.showDialog(null));
    }
}
