\NeedsTeXFormat{LaTeX2e}

\ProvidesClass{bmstu}[2022/11/20 v1.1 BMSTU class]


% Настройка документа ----------------------------------------------------------
% ------------------------------------------------------------------------------

% Установка базового класса
\LoadClass[a4paper, oneside, 14pt]{extreport}

% Настройка кодировки и языков
\RequirePackage[T1, T2A]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[english,main=russian]{babel}
%\RequirePackage{pscyr}
% \renewcommand{\rmdefault}{ftm}

% Настройка полей
\RequirePackage[
	left=30mm,
	right=15mm,
	top=20mm,
	bottom=20mm,
]{geometry}

% Настройка переносов
\RequirePackage{microtype}
\sloppy

% Настройка межстрочного интервала
\RequirePackage{setspace}
\onehalfspacing

% Настройка абзацного отступа
\RequirePackage{indentfirst}
\setlength{\parindent}{12.5mm}

% Заменить точки на штрихи в itemize
\usepackage{enumitem}
\renewcommand\labelitemi{---}

% Настройка заголовков
\makeatletter
\renewcommand\LARGE{\@setfontsize\LARGE{22pt}{20}}
\renewcommand\Large{\@setfontsize\Large{20pt}{20}}
\renewcommand\large{\@setfontsize\large{16pt}{20}}
\makeatother
\RequirePackage{titlesec}
\titleformat{\chapter}{\large\bfseries}{\thechapter}{14pt}{\large\bfseries}
\titleformat{name=\chapter,numberless}{}{}{0pt}{\large\bfseries\centering}
\titleformat{\section}{\large\bfseries}{\thesection}{14pt}{\large\bfseries}
\titleformat{\subsection}{\large\bfseries}{\thesubsection}{14pt}{\large\bfseries}
\titleformat{\subsubsection}{\large\bfseries}{\thesubsubsection}{14pt}{\large\bfseries}
\titlespacing{\chapter}{12.5mm}{-22pt}{10pt}
\titlespacing{\section}{12.5mm}{10pt}{10pt}
\titlespacing{\subsection}{12.5mm}{10pt}{10pt}
\titlespacing{\subsubsection}{12.5mm}{10pt}{10pt}
\setcounter{secnumdepth}{3}

% Подключения пакетов для фигур
\RequirePackage{graphicx}
\RequirePackage{float}
\RequirePackage{wrapfig}
\RequirePackage{tikzscale}

% Совмещение строк
\usepackage{multirow}

% Рисунки в svg
\usepackage{svg}

\RequirePackage{rotating}
\newcommand{\imgsvg}[6]
{
	\begin{figure}[#2]
		\fontsize{#4pt}{#5em}
		\center{\includesvg[scale=#3]{../img/#1}}
		\caption{#6}
		\label{img:#1}
	\end{figure}
}

% Создание рисунков
\RequirePackage{rotating}
\newcommand{\imgw}[4]
{
	\begin{figure}[#2]
		\center{\includegraphics[width=#3]{../img/#1}}
		\caption{#4}
		\label{img:#1}
	\end{figure}
}
\newcommand{\imgh}[4]
{
	\begin{figure}[#2]
		\center{\includegraphics[height=#3]{../img/#1}}
		\caption{#4}
		\label{img:#1}
	\end{figure}
}
\newcommand{\imgs}[4]
{
	\begin{figure}[#2]
		\center{\includegraphics[scale=#3]{../img/#1}}
		\caption{#4}
		\label{img:#1}
	\end{figure}
}
\newcommand{\imghw}[5]
{
	\begin{figure}[#2]
		\center{\includegraphics[height=#3, width=#4]{../img/#1}}
		\caption{#5}
		\label{img:#1}
	\end{figure}
}

\newcommand{\landimgw}[3]
{
	\center{\includegraphics[width=#2]{../img/#1}}
	\caption{#3}
	\label{img:#1}
}
\newcommand{\landimgh}[3]
{
	\center{\includegraphics[height=#2]{../img/#1}}
	\caption{#3}
	\label{img:#1}
}
\newcommand{\landimgs}[3]
{
	\center{\includegraphics[scale=#2]{../img/#1}}
	\caption{#3}
	\label{img:#1}
}

% Подключение пакетов таблиц
\RequirePackage{tabularx}
\RequirePackage{booktabs}
\RequirePackage{longtable}

% Настройка графиков
\RequirePackage{pgfplots}
\pgfplotsset{compat=newest}

% Настройка листингов
\RequirePackage[listings]{tcolorbox}
\tcbuselibrary{listings,breakable,minted,skins}
% изменение размера нумерации строк
\renewcommand\theFancyVerbLine{\scriptsize\arabic{FancyVerbLine}}
\newtcbinputlisting[auto counter,number within=chapter]{\mylisting}[6][]{
	% для отображение box title, если листинг на одной странице
	enhanced,
	% отступ перед листингом
	left skip=20pt,
	% рамка без закруглений
	arc=0mm,
	% тонкая рамка
	boxrule=1pt,
		listing only,
	listing file={../srcListings/#2},
	% стиль листинга
		listing engine=minted,
		minted language=#1,
		minted options = {
				linenos,
				breaklines=true,
				breakbefore=.,
				fontsize=\footnotesize\ttfamily,
				numbersep=7mm,
				firstnumber=1,
				% для firstline, lastline и др.
				#3
		},
	colback=white,
	colframe=black,
	breakable,
	% стиль основной подписи
	title={\parbox[t][][t]{3.5cm}{Листинг \thetcbcounter~---}\parbox[t][][t]{12.1cm}{#4}},
	attach boxed title to top left,
	% boxed title style={enhanced jigsaw, opacityfill=1, sharp corners, boxrule=0pt},
	boxed title style={enhanced jigsaw, opacityfill=1, sharp corners, boxrule=1pt, colframe=white},
	coltitle=black,
	colbacktitle=white,
	% подписи при переносе
	overlay first={
		\draw[line width=.5pt] (frame.south west)--(frame.south east);
	},
	enlarge top at break by = 0.8cm,
	overlay middle={
				\draw[line width=.5pt] (frame.south west)--(frame.south east);
				\draw[line width=.5pt] (frame.north west)--(frame.north east);
				\node[anchor=south west] at (frame.north west) {Продолжение листинга \thetcbcounter};
	},
	overlay last={
				\draw[line width=.5pt] (frame.north west)--(frame.north east);
				\node[anchor=south west] at (frame.north west) {Продолжение листинга \thetcbcounter};
	},
	label=lst:#5,
	#6
}

% Настройка подписей
\RequirePackage[
	labelsep=endash,
	figurename=Рисунок,
	singlelinecheck=false,
]{caption}
\captionsetup[figure]{justification=centering}

% Подключение пакетов для альбомной ориентации
\RequirePackage{lscape}
\RequirePackage{afterpage}

% Подключение математических пакетов
\RequirePackage{amsmath}
\RequirePackage{amssymb}

% Настройка библиографии
\RequirePackage[
	style=gost-numeric,
	language=auto,
	autolang=other,
	sorting=none,
]{biblatex}
\RequirePackage{csquotes}

% Подключение пакета для гиперссылок
\RequirePackage[unicode, hidelinks]{hyperref}

% Подключение пакета для управляющих конструкций
\RequirePackage{xifthen}


% Титульная страница -----------------------------------------------------------
% ------------------------------------------------------------------------------

% Установка мета-данных выходного файла
\newcommand{\documentmeta}[4]
{
	\hypersetup{
		pdftitle={#1 #2 #3},
		pdfsubject={#4},
		pdfauthor={#2}
	}
}

% Cоздание полей
\RequirePackage[normalem]{ulem}
\RequirePackage{stackengine}
\newcommand{\longunderline}[1]
{
	\uline{#1\hfill\mbox{}}
}
\newcommand{\fixunderline}[3]
{
	$\underset{\text{#3}}{\text{\uline{\stackengine{0pt}{\hspace{#2}}{\text{#1}}{O}{c}{F}{F}{L}}}}$
}

% Создание горизонтальной линии
\makeatletter
\newcommand{\vhrulefill}[1]
{
	\leavevmode\leaders\hrule\@height#1\hfill \kern\z@
}
\makeatother

% Создание шапки титульной страницы
\newcommand{\titlepageheader}[2]
{
	\begin{wrapfigure}[7]{l}{0.14\linewidth}
		\vspace{3.4mm}
		\hspace{-8mm}
		\includegraphics[width=0.89\linewidth]{bmstu-logo}
	\end{wrapfigure}
	
	{
		\singlespacing \small
		Министерство науки и высшего образования Российской Федерации \\
		Федеральное государственное автономное образовательное учреждение \\
		высшего образования \\
		<<Московский государственный технический университет \\
		имени Н.~Э.~Баумана \\
		(национальный исследовательский университет)>> \\
		(МГТУ им. Н.~Э.~Баумана) \\
	}
	
	\vspace{-4.2mm}
	\vhrulefill{0.9mm} \\
	\vspace{-7mm}
	\vhrulefill{0.2mm} \\
	\vspace{2.8mm}
	
	{
		\small
		ФАКУЛЬТЕТ ИУ \longunderline{<<#1>>} \\
		\vspace{3.3mm}
		КАФЕДРА ИУ-7 \longunderline{<<#2>>} \\
	}
}

% Установка заголовков РПЗ
\newcommand{\titlepagenotetitle}[2]
{
	{
		\LARGE \bfseries
		РАСЧЕТНО-ПОЯСНИТЕЛЬНАЯ ЗАПИСКА \\
	}
	\vspace{5mm}
	{
		\Large %\itshape
		\textit{#1 \\
		\vspace{5mm}
		НА ТЕМУ:} \\
		<<#2>> \\
	}
}

% Установка заголовков отчета
\newcommand{\titlepagereporttitle}[4]
{
	\textbf{ОТЧЕТ} \\
	\textbf{Лабораторная работа №}#1 \\
	\ifthenelse{\isempty{#2}}{}{по курсу <<#2>> \\}
	\ifthenelse{\isempty{#3}}{}{на тему: <<#3>> \\}
	\ifthenelse{\isempty{#4}}{}{Вариант №~#4 \\}
}

% Установка заголовков реферата
\newcommand{\titlepagesynopsistitle}[2]
{
	\textbf{РЕФЕРАТ} \\
	\ifthenelse{\isempty{#1}}{}{по курсу <<#1>> \\}
	\ifthenelse{\isempty{#2}}{}{на тему: <<#2>> \\}
}

% Установка заголовков домашнего задания
\newcommand{\titlepagehomeworktitle}[4]
{
	\textbf{ДОМАШНЕЕ ЗАДАНИЕ }#1 \\
	\ifthenelse{\isempty{#2}}{}{по курсу <<#2>> \\}
	\ifthenelse{\isempty{#3}}{}{на тему: <<#3>> \\}
	\ifthenelse{\isempty{#4}}{}{Вариант №~#4 \\}
}

% Создание поля студента
\newcommand{\titlepagestudent}[2]
{
	Студент \fixunderline{#1}{25mm}{(Группа)} &
	\fixunderline{}{40mm}{(Подпись, дата)} \vspace{1.3mm} &
	\fixunderline{#2}{40mm}{(И.~О.~Фамилия)} \\
}

% Создание прочих полей
\newcommand{\titlepageothers}[2]
{
	#1 &
	\fixunderline{}{40mm}{(Подпись, дата)} \vspace{1.3mm} &
	\fixunderline{#2}{40mm}{(И.~О.~Фамилия)} \\
}

% Установка исполнителей работы
\newcommand{\titlepageauthors}[7]
{
	{
		\small
		\begin{tabularx}{\textwidth}{@{}>{\hsize=.5\hsize}X>{\hsize=.25\hsize}X>{\hsize=.25\hsize}X@{}}
			\titlepagestudent{#1}{#2}
			\titlepageothers{#3}{#4}
			\ifthenelse{\isempty{#5}}{}{\titlepageothers{Консультант}{#5}}
			\ifthenelse{\isempty{#6}}{}{\titlepageothers{Консультант}{#6}}
			\ifthenelse{\isempty{#7}}{}{\titlepageothers{Нормоконтролер}{#7}}
		\end{tabularx}
	}
}

% Установка исполнителей работы (два автора)
\newcommand{\titlepagetwoauthors}[9]
{
	{
		\small
		\begin{tabularx}{\textwidth}{@{}>{\hsize=.5\hsize}X>{\hsize=.5\hsize}X>{\hsize=.25\hsize}X>{\hsize=.25\hsize}X@{}}
			\titlepagestudent{#1}{#2}
			\titlepagestudent{#3}{#4}
			\titlepageothers{#5}{#6}
			\ifthenelse{\isempty{#7}}{}{\titlepageothers{Консультант}{#7}}
			\ifthenelse{\isempty{#8}}{}{\titlepageothers{Консультант}{#8}}
			\ifthenelse{\isempty{#9}}{}{\titlepageothers{Нормоконтролер}{#9}}
		\end{tabularx}
	}
}

% Установка исполнителей работы (ДЛЯ ВКР)
\newcommand{\titlepageauthorsvkr}[5]
{
	{
		\small
		\begin{tabularx}{\textwidth}{@{}>{\hsize=.5\hsize}X>{\hsize=.25\hsize}X>{\hsize=.25\hsize}X@{}}
			\titlepagestudent{#1}{#2}
			\titlepageothers{#3}{#4}
			\titlepageothers{Нормоконтролер}{#5}
		\end{tabularx}
	}
}

% Создание титульной страницы РПЗ к ВКР
\makeatletter
\newcommand{\makethesistitle}[7]
{
	\documentmeta{РПЗ к ВКР}{#5}{#4}{#3}
	
	\begin{titlepage}
		\centering
		
		\titlepageheader{#1}{#2}
		\vspace{15.8mm}
		
		\titlepagenotetitle{К ВЫПУСКНОЙ КВАЛИФИКАЦИОННОЙ РАБОТЕ}{#3}
		\vfill
		
		\titlepageauthorsvkr{#4}{#5}{Руководитель ВКР}{#6}{#7}
		\vspace{14mm}
		
		\textit{{\the\year} г.}
	\end{titlepage}

	\setcounter{page}{2}
}
\makeatletter

% Создание титульной страницы РПЗ к КР
\makeatletter
\newcommand{\makecourseworktitle}[8]
{
	\documentmeta{РПЗ к КР}{#5}{#4}{#3}
	
	\begin{titlepage}
		\centering
		
		\titlepageheader{#1}{#2}
		\vspace{15.8mm}
		
		\titlepagenotetitle{К КУРСОВОЙ РАБОТЕ}{#3}
		\vfill
		
		\titlepageauthors{#4}{#5}{Руководитель курсовой работы}{#6}{#7}{#8}{}
		\vspace{14mm}
		
		\textit{{\the\year} г.}
	\end{titlepage}
	
	\setcounter{page}{2}
}
\makeatletter

% Создание титульной страницы РПЗ к КР с напарником
\makeatletter
\newcommand{\makecollectivecourseworktitle}[8]
{
	\documentmeta{РПЗ к КР}{#5}{#4}{#3}
	
	\begin{titlepage}
		\centering
		
		\titlepageheader{#1}{#2}
		\vspace{15.8mm}
		
		\titlepagenotetitle{К КУРСОВОЙ РАБОТЕ}{#3}
		\vfill
		
		\titlepagetwoauthors{#4}{#5}{#6}{#7}{Руководитель курсовой работы}{#8}{}{}{}
		\vspace{14mm}
		
		\textit{{\the\year} г.}
	\end{titlepage}
	
	\setcounter{page}{2}
}
\makeatletter

% Создание титульной страницы РПЗ к НИР
\makeatletter
\newcommand{\makeresearchworktitle}[8]
{
	\documentmeta{РПЗ к КР}{#5}{#4}{#3}
	
	\begin{titlepage}
		\centering
		
		\titlepageheader{#1}{#2}
		\vspace{15.8mm}
		
		\titlepagenotetitle{К НАУЧНО-ИССЛЕДОВАТЕЛЬСКОЙ РАБОТЕ}{#3}
		\vfill
		
		\titlepageauthors{#4}{#5}{Руководитель}{#6}{#7}{#8}{}
		\vspace{14mm}
		
		\textit{{\the\year} г.}
	\end{titlepage}
	
	\setcounter{page}{2}
}
\makeatletter

% Создание титульной страницы отчета
\makeatletter
\newcommand{\makereporttitle}[9]
{
	\documentmeta{Отчет}{#8}{#3 #4}{#5}
	
	\begin{titlepage}
		\centering
		
		\titlepageheader{#1}{#2}
		\vspace{15.8mm}
		
		\titlepagereporttitle{#3}{#4}{#5}{#6}
		\vfill
		
		\titlepageauthors{#7}{#8}{Преподаватель}{#9}{}{}{}
		\vspace{14mm}
		
		\textit{{\the\year} г.}
	\end{titlepage}
	
	\setcounter{page}{2}
}
\makeatletter

% Создание титульной страницы реферата
\makeatletter
\newcommand{\makesynopsistitle}[7]
{
	\documentmeta{Реферат}{#6}{#4}{#5}
	
	\begin{titlepage}
		\centering
		
		\titlepageheader{#1}{#2}
		\vspace{15.8mm}
		
		\titlepagesynopsistitle{#3}{#4}
		\vfill
		
		\titlepageauthors{#5}{#6}{Преподаватель}{#7}{}{}{}
		\vspace{14mm}
		
		\textit{{\the\year} г.}
	\end{titlepage}
	
	\setcounter{page}{2}
}
\makeatletter

% Создание титульной страницы домашнего задания
\makeatletter
\newcommand{\makehomeworktitle}[9]
{
	\documentmeta{Отчет}{#8}{#3 #4}{#5}
	
	\begin{titlepage}
		\centering
		
		\titlepageheader{#1}{#2}
		\vspace{15.8mm}
		
		\titlepagehomeworktitle{#3}{#4}{#5}{#6}
		\vfill
		
		\titlepageauthors{#7}{#8}{Преподаватель}{#9}{}{}{}
		\vspace{14mm}
		
		\textit{{\the\year} г.}
	\end{titlepage}
	
	\setcounter{page}{2}
}
\makeatletter


% Реферат ----------------------------------------------------------------------
% ------------------------------------------------------------------------------

% Подсчет количества страниц
\RequirePackage{lastpage}

% Подсчет количества рисунков и таблиц
\RequirePackage{etoolbox}
\newcounter{totfigures}
\newcounter{tottables}
\providecommand\totfig{}
\providecommand\tottab{}
\makeatletter
\AtEndDocument{%
	\addtocounter{totfigures}{\value{figure}}%
	\addtocounter{tottables}{\value{table}}%
	\immediate\write\@mainaux{%
		\string\gdef\string\totfig{\number\value{totfigures}}%
		\string\gdef\string\tottab{\number\value{tottables}}%
	}%
}
\makeatother
\pretocmd{\chapter}{\addtocounter{totfigures}{\value{figure}}\setcounter{figure}{0}}{}{}
\pretocmd{\chapter}{\addtocounter{tottables}{\value{table}}\setcounter{table}{0}}{}{}

% Подсчет количества использованных источников
\newcounter{totbibentries}
\newcommand*{\listcounted}{}
\providecommand\totbib{}
\makeatletter
\AtDataInput{%
	\xifinlist{\abx@field@entrykey}\listcounted%
	{}%
	{\stepcounter{totbibentries}%
		\listxadd\listcounted{\abx@field@entrykey}}%
}%
\makeatother

% Подсчет количества приложений
\usepackage{totcount, assoccnt}
\newcounter{appendixchapters}
\DeclareAssociatedCounters{chapter}{appendixchapters}
\regtotcounter{appendixchapters}

% Создание страницы реферата
\newenvironment{essay}[1]
{
	\chapter*{РЕФЕРАТ}
	\addcontentsline{toc}{chapter}{РЕФЕРАТ}
	
	Расчетно-пояснительная записка \begin{NoHyper}\pageref{LastPage}\end{NoHyper}~с., \totfig~рис., \tottab~табл., \thetotbibentries~источн., \total{appendixchapters}~прил.
	
	\noindent \MakeUppercase{#1} \par
}{}


% Содержание -------------------------------------------------------------------
% ------------------------------------------------------------------------------

% Создание содержания
\newcommand{\maketableofcontents}
{
	\renewcommand\contentsname{СОДЕРЖАНИЕ}
	\setcounter{tocdepth}{4}
	\tableofcontents
}

% Отточие у глав
\RequirePackage{tocloft}
\renewcommand{\cftchapleader}{\cftdotfill{\cftdotsep}}

% Настройка стиля заголовка содержания

% Стиль с выравниванием по центру
\renewcommand{\cfttoctitlefont}{\hfill\large\bfseries}
\renewcommand{\cftaftertoctitle}{\hfill\hfill}

% Отступы до и после
\setlength\cftbeforetoctitleskip{-22pt}
\setlength\cftaftertoctitleskip{15pt}

% Определения, обозначения и сокращения ----------------------------------------
% ------------------------------------------------------------------------------

% Создание элемента
\RequirePackage{enumitem}
\newcommand{\definition}[2]
{
	\item \noindent #1 --- #2
}

% Создание страницы определений
\newenvironment{definitions}
{
	\chapter*{ОПРЕДЕЛЕНИЯ}
	\addcontentsline{toc}{chapter}{ОПРЕДЕЛЕНИЯ}
	
	В настоящей расчетно-пояснительной записке применяют следующие термины с соответствующими определениями.
	
	\begin{description}[leftmargin=0pt]
}
{
	\end{description}
}

% Создание страницы обозначений и сокращений
\newenvironment{abbreviations}
{
	\chapter*{ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ}
	\addcontentsline{toc}{chapter}{ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ}
	
	В настоящем отчете применяют следующие сокращения и обозначения.
	
	\begin{description}[leftmargin=0pt]
}
{
	\end{description}
}

% Введение, заключение ---------------------------------------------------------
% ------------------------------------------------------------------------------

% Создание введения
\newcommand{\intro}
{
	\chapter*{ВВЕДЕНИЕ}
	\addcontentsline{toc}{chapter}{ВВЕДЕНИЕ}
}

% Создание заключение
\newcommand{\conclusion}
{
	\chapter*{ЗАКЛЮЧЕНИЕ}
	\addcontentsline{toc}{chapter}{ЗАКЛЮЧЕНИЕ}
}

% Создание главы без номера
\newcommand{\nonumchapter}[1]
{
	\chapter*{#1}
	\addcontentsline{toc}{chapter}{#1}
}


% Список использованных источников ---------------------------------------------
% ------------------------------------------------------------------------------

% Создание списка использованных источников
\newcommand{\makebibliography}
{
	\printbibliography[title=СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ]
	\addcontentsline{toc}{chapter}{СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ}
}


% Приложения -------------------------------------------------------------------
% ------------------------------------------------------------------------------

% Установка заголовков приложений
\RequirePackage[
	titletoc,
	title,
]{appendix}
\AtBeginDocument{\renewcommand{\appendixname}{ПРИЛОЖЕНИЕ}}

% Создание приложений
\let\oldappendices\appendices
\let\oldendappendices\endappendices
\renewenvironment{appendices}
{
	\titleformat{\chapter}{\large\bfseries}{\appendixname~\thechapter}{0pt}{\centering\large\bfseries\\}
	\setcounter{appendixchapters}{0}
	\oldappendices
	\renewcommand{\thechapter}{\Asbuk{chapter}}
}
{
	\oldendappendices
}
