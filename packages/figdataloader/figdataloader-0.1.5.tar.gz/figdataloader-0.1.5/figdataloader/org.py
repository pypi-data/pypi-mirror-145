def org(dataset_name="", *, fileconv: bool = False, countstart=0):
    import promptlib
    import os
    from pathlib import Path
    from PIL import Image
    import os
    import logging
    logging.basicConfig(filename="orgmessages.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if fileconv == True:
        prompter = promptlib.Files()
        if not prompter:
            return
        dir = prompter.dir()
        print(dir)
        for count, filename in enumerate(os.listdir(dir), countstart):
            dst = f"{str(dataset_name)}.{str(count)}.png"
            src = f"{dir}/{filename}"  # foldername/filename, si el archivo .py está fuera de la carpeta.
            dst = f"{dir}/{dst}"

            # rename() cambiará el nombre a los archivos.
            try:
                os.rename(src, dst)
            except FileExistsError:
                logger.info("File already exists.")
                break
        inputPath = Path(dir)
        inputFiles = inputPath.glob("**/*.png")
        outputPath = Path(dir)

        for f in inputFiles:
            outputFile = outputPath / Path(f.stem + ".jpg")
            im = Image.open(f)
            try:
                im.save(outputFile)
            except FileExistsError:
                logger.info("File already exists.")
        test = os.listdir(dir)
        for f2 in test:
            if f2.endswith(".png"):
                os.remove(os.path.join(dir, f2))
            elif FileNotFoundError:
                logger.info("File not found.")

    elif fileconv == False:
        prompter = promptlib.Files()
        if not prompter:
            return
        dir = prompter.dir()
        if not dir:
            return
        print(dir)
        for count, filename in enumerate(os.listdir(dir), countstart):
            dst = f"{str(dataset_name)}.{str(count)}.png"
            src = f"{dir}/{filename}"  # foldername/filename, si el archivo .py está fuera de la carpeta.
            dst = f"{dir}/{dst}"

            # rename() cambiará el nombre a los archivos.
            try:
                os.rename(src, dst)
            except FileExistsError:
                logger.info("File already exists.")
                break

if __name__ == '__main__':
    org()
