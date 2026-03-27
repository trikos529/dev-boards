import asyncio
import websockets
import json
import pyautogui

id_toggle = False
class_toggle = False
classification = ""
double_quotes = '""'
basic_tags = {"div", "h1", "h2", "h3", "p", "span", "ul", "ol", "li", "table", "tr", "td", "th", "form", "button", "label", "select", "option", "textarea", "header", "footer", "aside", "nav", "article", "main"}
video_audio_tags = {"video", "audio"}
css_properties = {"color", "font-size", "font-family", "font-weight", "text-align", "line-height", "text-decoration", "letter-spacing", "text-transform", "width", "height", "border-radius", "margin", "padding", "border", "display", "position", "flex-direction", "justify-content", "align-items", "flex-wrap", "gap", "flex", "grid-template-columns", "grid-template-rows", "background-color", "background-image", "background-size", "opacity", "box-shadow", "overflow", "cursor"}
reset_css = "* { margin: 0; padding: 0; box-sizing: border-box; }"
typescript_methods = {"width", "alt", "src", "disable", "required", "type", "value"}

async def main():
    async with websockets.serve(handle_droidpad, "0.0.0.0", 8765):
        print(f"WebSocket server running on ws://0.0.0.0:8765")
        print("Press Ctrl+C to stop the server")
        await asyncio.Future()

async def handle_droidpad(websocket):
    global id_toggle, class_toggle, classification, basic_tags, video_audio_tags, double_quotes, css_properties, typescript_methods
    print("Device Linked!")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get("type")
                state = data.get("state")
                btn_id = data.get("id")
                print(f"Received: {btn_id}")
                
                if btn_id == "id_state":
                    if id_toggle == True:
                        id_toggle = False
                    else:
                        id_toggle = True
                    if class_toggle == False and id_toggle == False:
                        classification = ""
                    elif class_toggle == True:
                        classification = " class=\"\""
                    elif id_toggle == True:
                        classification = " id=\"\""
                    else:
                        classification = " id=\"\" class=\"\""
                    
                elif btn_id == "class_state":
                    if class_toggle == True:
                        class_toggle = False
                    else:
                        class_toggle = True
                    if class_toggle == False and id_toggle == False:
                        classification = ""
                    elif class_toggle == True:
                        classification = " class=\"\""
                    elif id_toggle == True:
                        classification = " id=\"\""
                    else:
                        classification = " id=\"\" class=\"\""

                # HTML Tags
                elif btn_id in basic_tags:
                    pyautogui.write(f"<{btn_id} {classification}><{btn_id}/>")
                elif btn_id == "a":
                    pyautogui.write(f"<a href={double_quotes} {classification}>")
                elif btn_id == "img":
                    pyautogui.write(f"<img src={double_quotes} {classification}>")
                elif btn_id in video_audio_tags:
                    pyautogui.write(f"<{btn_id} {classification}><{btn_id}/>")
                # CSS Tags
                elif btn_id in css_properties:
                    pyautogui.write(f"{btn_id}:")
                elif btn_id == "css-reset":
                    pyautogui.write(reset_css)
                # TS Tags
                elif btn_id == "get-element-id":
                    pyautogui.write(f"=document.getElementById({double_quotes});")
                elif btn_id == "get-element-class": 
                    pyautogui.write(f"= document.getElementsByClassName({double_quotes});")
                elif btn_id == "get-element-type":
                    pyautogui.write(f"= document.getElementsByTagName({double_quotes});")
                elif btn_id in typescript_methods:
                    pyautogui.write(f".{btn_id}= ;")
                    
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                continue
            except Exception as e:
                print(f"Error processing message: {e}")
                continue
                
    except websockets.exceptions.ConnectionClosed:
        print("Device disconnected")
    except Exception as e:
        print(f"Error in connection: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user
