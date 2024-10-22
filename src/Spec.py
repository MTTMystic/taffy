#TODO ensure to add continue on error in future iterations after code is verified working
class Spec:
    def __init__(self, output_dir, taffy_gen_output_dir, use_sfo, create_dir):
        self.output_dir = output_dir
        self.taffy_gen_output_dir = taffy_gen_output_dir
        self.use_sfo = use_sfo
        self.create_dir = create_dir
    