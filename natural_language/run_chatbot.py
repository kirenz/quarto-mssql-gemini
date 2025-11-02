from app_df import combined_interface

if __name__ == "__main__":
    combined_interface.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860,
        show_api=False
    )
