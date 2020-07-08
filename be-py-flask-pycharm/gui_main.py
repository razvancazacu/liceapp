from tkinter import *

import gui_controller

if __name__ == '__main__':
    root = Tk()
    root.title("Control")
    root.geometry("440x450")
    Controller = gui_controller.MainControl()

    selected_local_pdf = StringVar(root)
    selected_download_option = StringVar(root)

    selected_local_pdf.set("Select PDF for conversion")
    selected_download_option.set("latest")

    myButtonAutoStart = Button(
        root, text="(1)AutoStart (Steps 2,5,6,3)", width=30, height=3,
        command=lambda: Controller.auto_start())
    myButtonServerStart = Button(
        root, text="(2)Start Server", width=30, height=3,
        command=lambda: Controller.start_server())
    myButtonExtractDataFromImages = Button(
        root, text="(3)Extract Data From Existing JPEGs", width=30, height=3,
        command=lambda: Controller.extract_data())

    myButtonAutoStartTimer = Button(
        root, text="(4.1)AutoExtract On Interval(Steps 5,6,3)", width=30, height=3,
        command=lambda: Controller.auto_extract_on_timer_sleeper())
    myButtonAutoStartTimerSTOP = Button(
        root, text="(4.2)Stop AutoExtract On Interval", width=30, height=3,
        command=lambda: Controller.stop_extraction_on_interval())
    myButtonDownloadPDF = Button(
        root, text="(5)Download PDF From FMI", width=30, height=3,
        command=lambda: Controller.download_pdf())
    myButtonExtractImages = Button(
        root, text="(6)Extract Images From The Selected PDF", width=30, height=3,
        command=lambda: Controller.convert_pdf_to_img())
    myButtonWriteToJson = Button(
        root, text="(7)Extract Data To JSON", width=30, height=3,
        command=lambda: Controller.write_schedule_toJSON())
    myButtonCloseServer = Button(
        root, text="(8)Close Server", width=30, height=3,
        command=lambda: Controller.close_server())
    myButtonCloseGUI = Button(
        root, text="(9)EXIT", width=30, height=3,
        command=lambda: exit_gui())

    dropSelectedPDF = OptionMenu(
        root, selected_local_pdf, *Controller.get_local_pdfs())
    dropSelectedDownloadOption = OptionMenu(
        root, selected_download_option, 'latest', 's1', 's2')

    myButtonAutoStart.grid(row=1, sticky="ew")
    myButtonServerStart.grid(row=2, sticky="ew")
    myButtonExtractDataFromImages.grid(row=3, sticky="ew")
    myButtonAutoStartTimer.grid(row=4, sticky="ew")
    myButtonAutoStartTimerSTOP.grid(row=4, column=1, sticky="ew")
    myButtonDownloadPDF.grid(row=5, sticky="ew")
    dropSelectedDownloadOption.grid(row=5, column=1, sticky="ew")
    myButtonExtractImages.grid(row=6, sticky="ew")
    dropSelectedPDF.grid(row=6, column=1, sticky="ew")
    myButtonWriteToJson.grid(row=7, sticky="ew")
    myButtonCloseServer.grid(row=8, sticky="ew")
    myButtonCloseGUI.grid(row=9, sticky="ew")


    def exit_gui():
        Controller.close_server()
        root.destroy()


    def change_dropdown_pdf(*args):
        dropSelectedPDF.children["menu"].delete(0, "end")
        for pdf in Controller.get_local_pdfs():
            dropSelectedPDF.children["menu"].add_command(label=pdf,
                                                         command=lambda pdfl=pdf: selected_local_pdf.set(pdfl))
        Controller.current_pdf = selected_local_pdf.get()
        print("Current PDF Changed to:", Controller.current_pdf)


    def change_dropdown_download_option(*args):
        Controller.pdf_option = selected_download_option.get()
        print("Download option changed to:", selected_download_option.get())


    selected_download_option.trace('w', change_dropdown_download_option)
    selected_local_pdf.trace('w', change_dropdown_pdf)
    root.mainloop()
