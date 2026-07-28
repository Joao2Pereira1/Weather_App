# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 480)
        MainWindow.setMinimumSize(QtCore.QSize(850, 450))

        # Estilo injetado a partir do ficheiro python em vez de file.qss
        MainWindow.setStyleSheet("""
            QMainWindow {
                background-color: #F4F6F9;
            }
            QLabel {
                font-family: 'Segoe UI', Helvetica, Arial;
                color: #2C3E50;
            }
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                color: #334155;
            }
            QLineEdit:focus {
                border: 2px solid #3B82F6;
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 18px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
            QLabel#locationLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1E293B;
            }
            QLabel#locationInfoLabel {
                background-color: #E2E8F0;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
                color: #475569;
            }
            /* Estilização dos Cards Semanais */
            QFrame[objectName^="card"] {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            QLabel[objectName^="lbl_day"] {
                font-size: 14px;
                font-weight: bold;
                color: #64748B;
            }
            QLabel[objectName^="lbl_temp"] {
                font-size: 15px;
                font-weight: 600;
                color: #0F172A;
            }
            /* Menus e Barras */
            QMenuBar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E2E8F0;
                color: #334155;
            }
            QMenuBar::item:selected {
                background-color: #F1F5F9;
            }
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
            }
            QMenu::item:selected {
                background-color: #F1F5F9;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout principal da janela
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(15)

        # Zona Superior: Busca
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.setSpacing(10)

        self.locationLabel = QtWidgets.QLabel(self.centralwidget)
        self.locationLabel.setObjectName("locationLabel")
        self.searchLayout.addWidget(self.locationLabel)

        self.locationInput = QtWidgets.QLineEdit(self.centralwidget)
        self.locationInput.setPlaceholderText("Digite a cidade (ex: Lisboa, London)...")
        self.searchLayout.addWidget(self.locationInput)

        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setObjectName("searchButton")
        self.searchLayout.addWidget(self.searchButton)

        self.mainLayout.addLayout(self.searchLayout)

        # Zona Intermédia: Informaçoes extras do local ativo
        self.locationInfoLabel = QtWidgets.QLabel(self.centralwidget)
        self.locationInfoLabel.setObjectName("locationInfoLabel")
        self.locationInfoLabel.setWordWrap(True)
        self.mainLayout.addWidget(self.locationInfoLabel)

        # Zona Inferior: Título e Grid da Previsão Semanal
        self.forecastTitle = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.forecastTitle.setFont(font)
        self.mainLayout.addWidget(self.forecastTitle)

        # Container dos Cards
        self.weekLayout = QtWidgets.QHBoxLayout()
        self.weekLayout.setSpacing(12)

        # Dados estruturados dos dias para criacao dinâmica e limpa dos cartoes
        self.days_data = [
            ("Segunda", "32ºC / 40ºC"),
            ("Terça", "22ºC / 30ºC"),
            ("Quarta", "18ºC / 30ºC"),
            ("Quinta", "10ºC / 20ºC"),
            ("Sexta", "30ºC / 40ºC"),
            ("Sábado", "12ºC / 22ºC"),
            ("Domingo", "30ºC / 40ºC"),
        ]

        # Loop de geracao dos cartoes verticais (Dia -> Ícone -> Temp)
        for i, (day_name, temp_val) in enumerate(self.days_data, 1):
            card = QtWidgets.QFrame(self.centralwidget)
            card.setObjectName(f"card_{i}")

            cardLayout = QtWidgets.QVBoxLayout(card)
            cardLayout.setContentsMargins(10, 15, 10, 15)
            cardLayout.setSpacing(10)
            cardLayout.setAlignment(QtCore.Qt.AlignCenter)

            lbl_day = QtWidgets.QLabel(day_name, card)
            lbl_day.setObjectName(f"lbl_day_{i}")
            lbl_day.setAlignment(QtCore.Qt.AlignCenter)
            cardLayout.addWidget(lbl_day)

            lbl_icon = QtWidgets.QLabel(card)
            lbl_icon.setObjectName(f"lbl_icon_{i}")
            lbl_icon.setMinimumSize(QtCore.QSize(48, 48))
            lbl_icon.setAlignment(QtCore.Qt.AlignCenter)
            # Placeholder para receber o QPixmap com o ícone da API de clima posteriormente
            lbl_icon.setText("---")
            cardLayout.addWidget(lbl_icon)

            lbl_temp = QtWidgets.QLabel(temp_val, card)
            lbl_temp.setObjectName(f"lbl_temp_{i}")
            lbl_temp.setAlignment(QtCore.Qt.AlignCenter)
            cardLayout.addWidget(lbl_temp)

            self.weekLayout.addWidget(card)

            # Guardar referências dinamicas no objeto para controle posterior via API
            setattr(self, f"day_{i}", lbl_day)
            setattr(self, f"icon_{i}", lbl_icon)
            setattr(self, f"temperature_{i}", lbl_temp)

        self.mainLayout.addLayout(self.weekLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        # Menubar e Statusbar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 25))
        self.weatherMenu = QtWidgets.QMenu(self.menubar)
        self.weatherMenu.setObjectName("weatherMenu")
        self.helpMenu = QtWidgets.QMenu(self.menubar)
        self.helpMenu.setObjectName("helpMenu")
        MainWindow.setMenuBar(self.menubar)

        # Opções para weather Menu (Refresh,Current location,Exit)
        self.actionRefresh = QtWidgets.QAction(MainWindow)
        self.actionCurrentLocation = QtWidgets.QAction(MainWindow)
        self.actionExit = QtWidgets.QAction(MainWindow)

        self.weatherMenu.addAction(self.actionRefresh)
        self.weatherMenu.addAction(self.actionCurrentLocation)
        self.weatherMenu.addSeparator()
        self.weatherMenu.addAction(self.actionExit)

        # Opções para help Menu (Help,About)
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionAbout = QtWidgets.QAction(MainWindow)

        self.helpMenu.addAction(self.actionHelp)
        self.helpMenu.addAction(self.actionAbout)

        # Adicionar o weather menu e about menu à aplicacao
        self.menubar.addAction(self.weatherMenu.menuAction())
        self.menubar.addAction(self.helpMenu.menuAction())

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Previsão do Tempo"))
        self.locationLabel.setText(_translate("MainWindow", "Localização"))
        self.searchButton.setText(_translate("MainWindow", "Procurar"))
        self.locationInfoLabel.setText(
            _translate(
                "MainWindow",
                "Aguardando pesquisa de localização... Aqui aparecerão coordenadas e vento.",
            )
        )
        self.forecastTitle.setText(_translate("MainWindow", "Previsão para a semana"))

        self.weatherMenu.setTitle(_translate("MainWindow", "Clima"))
        self.helpMenu.setTitle(_translate("MainWindow", "Ajuda"))

        self.actionRefresh.setText(_translate("MainWindow", "Atualizar"))
        self.actionCurrentLocation.setText(
            _translate("MainWindow", "Localização Atual")
        )
        self.actionExit.setText(_translate("MainWindow", "Sair"))

        self.actionHelp.setText(_translate("MainWindow", "Ajuda"))
        self.actionAbout.setText(_translate("MainWindow", "Acerca de"))
