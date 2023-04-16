from deeppavlov import build_model

model = build_model('en_odqa_bpr_croped_fid')

# model = torch.load('model.pt')
# with open('vocab.pkl', 'rb') as f:
    # vocab = pickle.load(f)
# tokenizer = get_tokenizer('basic_english')
